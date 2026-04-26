from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "cambia-esta-clave-en-produccion"

MAX_INTENTOS = 3

@app.route("/")
def inicio():
    intentos = session.get("intentos_fallidos", 0)
    bloqueado = intentos >= MAX_INTENTOS
    return render_template(
        "login.html",
        mensaje="",
        intentos=intentos,
        max_intentos=MAX_INTENTOS,
        bloqueado=bloqueado,
    )

@app.route("/login", methods=["POST"])
def login():
    intentos = session.get("intentos_fallidos", 0)
    if intentos >= MAX_INTENTOS:
        return render_template(
            "login.html",
            mensaje="Llegaste al maximo de intentos. Acceso bloqueado.",
            intentos=intentos,
            max_intentos=MAX_INTENTOS,
            bloqueado=True,
        )

    usuario = request.form.get("usuario")
    clave = request.form.get("clave")

    if usuario == "admin" and clave == "1234":
        session["intentos_fallidos"] = 0
        return f"<h1>Bienvenido, {usuario}</h1><p>Acceso correcto.</p>"
    else:
        intentos += 1
        session["intentos_fallidos"] = intentos
        bloqueado = intentos >= MAX_INTENTOS
        if bloqueado:
            mensaje = "Llegaste al maximo de intentos. Acceso bloqueado."
        else:
            mensaje = f"Usuario o contrasena incorrectos. Intento {intentos} de {MAX_INTENTOS}."

        return render_template(
            "login.html",
            mensaje=mensaje,
            intentos=intentos,
            max_intentos=MAX_INTENTOS,
            bloqueado=bloqueado,
        )

if __name__ == "__main__":
    app.run(debug=True)
