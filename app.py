from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps
import pymysql


app = Flask(__name__)
app.secret_key = "chave-super-secreta-aqui"  # troque depois


# ---------- CONEXÃO COM O BANCO ----------

def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="Industrias_Wayne",
        cursorclass=pymysql.cursors.DictCursor
    )


# -------- DECORATOR PARA EXIGIR LOGIN --------

def login_required(view_func):
    @wraps(view_func)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view_func(*args, **kwargs)
    return wrapper


# ---------- ROTA DE LOGIN ----------

@app.route("/login", methods=["GET", "POST"])
def login():
    # GET → mostra formulário
    if request.method == "GET":
        return render_template("login.html")

    # POST → processa formulário
    email = request.form.get("email")
    senha = request.form.get("senha")

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM usuarios WHERE email = %s AND senha = %s AND ativo = 1",
                (email, senha)
            )
            user = cur.fetchone()

        if user:
            session["user_id"] = user["id"]
            session["tipo_perfil"] = user["tipo_perfil"]

            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO logs_acessos (usuario_id, tipo_acao, detalhes) "
                    "VALUES (%s, %s, %s)",
                    (user["id"], "login_sucesso", "Login via painel WTSA")
                )
            conn.commit()
            return redirect(url_for("dashboard"))
        else:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO logs_acessos (usuario_id, tipo_acao, detalhes) "
                    "VALUES (NULL, %s, %s)",
                    ("login_falha", f"Tentativa com email {email}")
                )
            conn.commit()
            return render_template("login.html", erro="Credenciais inválidas")
    finally:
        conn.close()


# ---------- DASHBOARD ----------

@app.route("/")
@login_required
def home():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # ---------- CARDS SUPERIORES ----------
            # usuários ativos
            cur.execute("SELECT COUNT(*) AS total FROM usuarios WHERE ativo = 1")
            total_usuarios = cur.fetchone()["total"]

            # recursos cadastrados
            try:
                cur.execute("SELECT COUNT(*) AS total FROM recursos")
                total_recursos = cur.fetchone()["total"]
            except Exception:
                total_recursos = 0

            # total de alertas (logs de falha/acesso negado)
            cur.execute("""
                SELECT COUNT(*) AS total
                FROM logs_acessos
                WHERE tipo_acao IN ('login_falha', 'acesso_negado')
            """)
            total_alertas = cur.fetchone()["total"]

            # acessos hoje = logins de hoje
            cur.execute("""
                SELECT COUNT(*) AS total
                FROM logs_acessos
                WHERE tipo_acao = 'login_sucesso'
                  AND DATE(data_hora) = CURDATE()
            """)
            acessos_hoje = cur.fetchone()["total"]

            # ---------- ACESSOS POR DIA (ÚLTIMOS 7 DIAS) ----------
            cur.execute("""
                SELECT
                    DAYOFWEEK(data_hora) AS dow,
                    COUNT(*) AS total
                FROM logs_acessos
                WHERE tipo_acao = 'login_sucesso'
                  AND data_hora >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
                GROUP BY DAYOFWEEK(data_hora)
            """)
            rows = cur.fetchall()

            # mapeia dow MySQL (1=Dom, 2=Seg...) para índice 0..6 (Seg..Dom)
            acessos_por_dia = {d: 0 for d in ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]}
            for r in rows:
                dow = r["dow"]
                if dow == 1:
                    chave = "dom"
                elif dow == 2:
                    chave = "seg"
                elif dow == 3:
                    chave = "ter"
                elif dow == 4:
                    chave = "qua"
                elif dow == 5:
                    chave = "qui"
                elif dow == 6:
                    chave = "sex"
                else:
                    chave = "sab"
                acessos_por_dia[chave] = r["total"]

            max_acessos = max(acessos_por_dia.values()) if acessos_por_dia.values() else 1
            # normaliza em porcentagem para altura das barras
            acessos_por_dia_pct = {
                dia: (valor / max_acessos) * 100 if max_acessos > 0 else 0
                for dia, valor in acessos_por_dia.items()
            }

            # ---------- INCIDENTES POR MÊS (ÚLTIMOS 6 MESES) ----------
            cur.execute("""
                SELECT
                    DATE_FORMAT(data_hora, '%Y-%m') AS ano_mes,
                    DATE_FORMAT(data_hora, '%b') AS mes_label,
                    COUNT(*) AS total
                FROM movimentacoes_recursos
                WHERE data_hora >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
                GROUP BY ano_mes
                ORDER BY ano_mes
            """)
            incidentes_rows = cur.fetchall()

            incidentes_meses = [r["mes_label"] for r in incidentes_rows]
            incidentes_totais = [r["total"] for r in incidentes_rows]
            max_incidentes = max(incidentes_totais) if incidentes_totais else 1
            incidentes_pct = [
                (v / max_incidentes) * 100 if max_incidentes > 0 else 0
                for v in incidentes_totais
            ]

            # ---------- DISTRIBUIÇÃO DE RECURSOS ----------
            cur.execute("""
                SELECT categoria, COUNT(*) AS total
                FROM recursos
                GROUP BY categoria
            """)
            dist_rows = cur.fetchall()
            total_recursos_dist = sum(r["total"] for r in dist_rows) or 1

            dist_categorias = []
            for r in dist_rows:
                dist_categorias.append({
                    "categoria": r["categoria"],
                    "total": r["total"],
                    "pct": (r["total"] / total_recursos_dist) * 100
                })

            # ---------- ATIVIDADE RECENTE (MISTO) ----------
            # pega alguns registros de logs_acessos e movimentacoes_recursos
            cur.execute("""
                SELECT
                    data_hora,
                    CONCAT('Login ', tipo_acao) AS titulo,
                    detalhes AS subtitulo
                FROM logs_acessos
                ORDER BY data_hora DESC
                LIMIT 5
            """)
            atividades_logs = cur.fetchall()

            cur.execute("""
                SELECT
                    mr.data_hora,
                    CONCAT('Recurso ', mr.tipo_movimentacao) AS titulo,
                    r.nome AS subtitulo
                FROM movimentacoes_recursos mr
                JOIN recursos r ON r.id = mr.recurso_id
                ORDER BY mr.data_hora DESC
                LIMIT 5
            """)
            atividades_recursos = cur.fetchall()

            atividades = atividades_logs + atividades_recursos
            atividades = sorted(atividades, key=lambda x: x["data_hora"], reverse=True)[:5]

        return render_template(
            "dashboard.html",
            total_usuarios=total_usuarios,
            total_recursos=total_recursos,
            total_alertas=total_alertas,
            acessos_hoje=acessos_hoje,
            acessos_por_dia_pct=acessos_por_dia_pct,
            acessos_por_dia=acessos_por_dia,
            incidentes_meses=incidentes_meses,
            incidentes_totais=incidentes_totais,
            incidentes_pct=incidentes_pct,
            dist_categorias=dist_categorias,
            atividades=atividades,
        )
    finally:
        conn.close()



# ---------- CRUD DE USUÁRIOS ----------

@app.route("/users")
@login_required
def users():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    u.id,
                    u.nome,
                    u.email,
                    u.tipo_perfil,
                    u.ativo,
                    MAX(CASE
                        WHEN l.tipo_acao = 'login_sucesso' THEN l.data_hora
                        ELSE NULL
                    END) AS ultimo_login
                FROM usuarios u
                LEFT JOIN logs_acessos l
                    ON l.usuario_id = u.id
                GROUP BY
                    u.id, u.nome, u.email, u.tipo_perfil, u.ativo
                ORDER BY
                    u.ativo DESC,
                    u.nome ASC
            """)
            usuarios = cur.fetchall()
        return render_template("users.html", usuarios=usuarios)
    finally:
        conn.close()


@app.route("/users/new", methods=["GET", "POST"])
@login_required
def new_user():
    conn = get_connection()
    try:
        if request.method == "POST":
            nome = request.form.get("nome")
            email = request.form.get("email")
            senha = request.form.get("senha")
            tipo_perfil = request.form.get("tipo_perfil")
            ativo = 1 if request.form.get("ativo") == "on" else 0

            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO usuarios (nome, email, senha, tipo_perfil, ativo)
                    VALUES (%s, %s, %s, %s, %s)
                """, (nome, email, senha, tipo_perfil, ativo))
            conn.commit()
            return redirect(url_for("users"))

        return render_template("edit_user.html", user=None)
    finally:
        conn.close()


@app.route("/users/<int:user_id>/edit", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            if request.method == "POST":
                nome = request.form.get("nome")
                email = request.form.get("email")
                senha = request.form.get("senha")
                tipo_perfil = request.form.get("tipo_perfil")
                ativo = 1 if request.form.get("ativo") == "on" else 0

                # se senha vier vazia, não altera a senha
                if senha:
                    cur.execute("""
                        UPDATE usuarios
                        SET nome = %s,
                            email = %s,
                            senha = %s,
                            tipo_perfil = %s,
                            ativo = %s
                        WHERE id = %s
                    """, (nome, email, senha, tipo_perfil, ativo, user_id))
                else:
                    cur.execute("""
                        UPDATE usuarios
                        SET nome = %s,
                            email = %s,
                            tipo_perfil = %s,
                            ativo = %s
                        WHERE id = %s
                    """, (nome, email, tipo_perfil, ativo, user_id))

                conn.commit()
                return redirect(url_for("users"))

            # GET → busca dados do usuário
            cur.execute("""
                SELECT id, nome, email, tipo_perfil, ativo
                FROM usuarios
                WHERE id = %s
            """, (user_id,))
            user = cur.fetchone()

        if not user:
            return redirect(url_for("users"))

        return render_template("edit_user.html", user=user)
    finally:
        conn.close()


@app.route("/users/<int:user_id>/toggle", methods=["POST"])
@login_required
def toggle_user(user_id):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT ativo FROM usuarios WHERE id = %s", (user_id,))
            row = cur.fetchone()
            if not row:
                return redirect(url_for("users"))

            novo_status = 0 if row["ativo"] else 1
            cur.execute("UPDATE usuarios SET ativo = %s WHERE id = %s", (novo_status, user_id))
        conn.commit()
        return redirect(url_for("users"))
    finally:
        conn.close()


# ---------- CRUD DE RECURSOS ----------

@app.route("/resources")
@login_required
def resources():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    id,
                    nome,
                    categoria,
                    descricao,
                    status,
                    localizacao,
                    observacoes_adicionais
                FROM recursos
                ORDER BY id ASC
            """)
            recursos = cur.fetchall()
        return render_template("resources.html", recursos=recursos)
    finally:
        conn.close()


@app.route("/resources/new", methods=["GET", "POST"])
@login_required
def new_resource():
    conn = get_connection()
    try:
        if request.method == "POST":
            nome = request.form.get("nome")
            categoria = request.form.get("categoria")
            descricao = request.form.get("descricao")
            status = request.form.get("status")
            localizacao = request.form.get("localizacao")
            observacoes_adicionais = request.form.get("observacoes_adicionais")

            with conn.cursor() as cur:
                # insere recurso
                cur.execute("""
                    INSERT INTO recursos (nome, categoria, descricao, status, localizacao, observacoes_adicionais)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (nome, categoria, descricao, status, localizacao, observacoes_adicionais))
                recurso_id = cur.lastrowid

                # registra movimentação: cadastrado
                cur.execute("""
                    INSERT INTO movimentacoes_recursos (recurso_id, usuario_id, tipo_movimentacao)
                    VALUES (%s, %s, %s)
                """, (recurso_id, session.get("user_id"), "cadastrado"))

            conn.commit()
            return redirect(url_for("resources"))

        return render_template("edit_resource.html", recurso=None)
    finally:
        conn.close()


@app.route("/resources/<int:recurso_id>/edit", methods=["GET", "POST"])
@login_required
def edit_resource(recurso_id):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            if request.method == "POST":
                nome = request.form.get("nome")
                categoria = request.form.get("categoria")
                descricao = request.form.get("descricao")
                status = request.form.get("status")
                localizacao = request.form.get("localizacao")
                observacoes_adicionais = request.form.get("observacoes_adicionais")

                # atualiza recurso
                cur.execute("""
                    UPDATE recursos
                    SET nome = %s,
                        categoria = %s,
                        descricao = %s,
                        status = %s,
                        localizacao = %s,
                        observacoes_adicionais = %s
                    WHERE id = %s
                """, (nome, categoria, descricao, status, localizacao, observacoes_adicionais, recurso_id))

                # registra movimentação: atualizado
                cur.execute("""
                    INSERT INTO movimentacoes_recursos (recurso_id, usuario_id, tipo_movimentacao)
                    VALUES (%s, %s, %s)
                """, (recurso_id, session.get("user_id"), "atualizado"))

                conn.commit()
                return redirect(url_for("resources"))

            cur.execute("""
                SELECT
                    id,
                    nome,
                    categoria,
                    descricao,
                    status,
                    localizacao,
                    observacoes_adicionais
                FROM recursos
                WHERE id = %s
            """, (recurso_id,))
            recurso = cur.fetchone()

        if not recurso:
            return redirect(url_for("resources"))

        return render_template("edit_resource.html", recurso=recurso)
    finally:
        conn.close()


@app.route("/resources/<int:recurso_id>/toggle", methods=["POST"])
@login_required
def toggle_resource(recurso_id):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT status FROM recursos WHERE id = %s", (recurso_id,))
            row = cur.fetchone()
            if not row:
                return redirect(url_for("resources"))

            status_atual = row["status"]
            # alterna entre ativo e desativado; se estiver em_manutencao ou outro, vai para ativo
            if status_atual == "desativado":
                novo_status = "ativo"
            else:
                novo_status = "desativado"

            # atualiza recurso
            cur.execute("UPDATE recursos SET status = %s WHERE id = %s", (novo_status, recurso_id))

            # registra movimentação: desativado (usando esse tipo para toggle)
            cur.execute("""
                INSERT INTO movimentacoes_recursos (recurso_id, usuario_id, tipo_movimentacao)
                VALUES (%s, %s, %s)
            """, (recurso_id, session.get("user_id"), "desativado"))

        conn.commit()
        return redirect(url_for("resources"))
    finally:
        conn.close()


# ---------- SEGURANÇA ----------

@app.route("/security")
@login_required
def security():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # Incidentes recentes = movimentações de recursos
            cur.execute("""
                SELECT
                    mr.id,
                    mr.tipo_movimentacao,
                    mr.data_hora,
                    r.nome AS recurso_nome,
                    r.localizacao
                FROM movimentacoes_recursos mr
                JOIN recursos r ON r.id = mr.recurso_id
                ORDER BY mr.data_hora DESC
                LIMIT 10
            """)
            incidentes = cur.fetchall()

            # Alertas de segurança = logs de acessos com falha/negado
            cur.execute("""
                SELECT
                    l.id,
                    l.tipo_acao,
                    l.data_hora,
                    l.detalhes,
                    u.nome AS usuario_nome
                FROM logs_acessos l
                LEFT JOIN usuarios u ON u.id = l.usuario_id
                WHERE l.tipo_acao IN ('login_falha', 'acesso_negado')
                ORDER BY l.data_hora DESC
                LIMIT 10
            """)
            alertas = cur.fetchall()

        return render_template("security.html", incidentes=incidentes, alertas=alertas)
    finally:
        conn.close()

@app.route("/security/incidents/new", methods=["GET", "POST"])
@login_required
def new_incident():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            # para o select de recursos no formulário
            cur.execute("""
                SELECT id, nome, localizacao
                FROM recursos
                ORDER BY nome ASC
            """)
            recursos = cur.fetchall()

        if request.method == "POST":
            recurso_id = request.form.get("recurso_id")
            tipo_movimentacao = request.form.get("tipo_movimentacao")
            detalhes = request.form.get("detalhes")

            conn2 = get_connection()
            try:
                with conn2.cursor() as cur2:
                    # insere incidente manual
                    cur2.execute("""
                        INSERT INTO movimentacoes_recursos (recurso_id, usuario_id, tipo_movimentacao)
                        VALUES (%s, %s, %s)
                    """, (recurso_id, session.get("user_id"), tipo_movimentacao))
                    # se quiser guardar detalhes em outra coluna depois, é só adicionar na tabela
                conn2.commit()
            finally:
                conn2.close()

            return redirect(url_for("security"))

        return render_template("new_incident.html", recursos=recursos)
    finally:
        conn.close()



# ---------- ENTRADA ----------

if __name__ == "__main__":
    app.run(debug=True)
