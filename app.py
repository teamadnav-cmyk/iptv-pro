from flask import Flask, Response, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# -----------------------------
# Database Model
# -----------------------------
class Stream(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    url = db.Column(db.Text)
    group = db.Column(db.String(100))

with app.app_context():
    db.create_all()

# -----------------------------
# Playlist Generator
# -----------------------------
@app.route("/playlist.m3u")
def playlist():
    streams = Stream.query.all()
    m3u = "#EXTM3U\n"

    for s in streams:
        m3u += f'#EXTINF:-1 group-title="{s.group}",{s.name}\n'
        m3u += f'{s.url}\n'

    return Response(
        m3u,
        mimetype="audio/x-mpegurl",
        headers={"Cache-Control": "no-cache"}
    )

# -----------------------------
# Admin Panel
# -----------------------------
@app.route("/")
def admin():
    streams = Stream.query.all()
    return render_template("admin.html", streams=streams)

# -----------------------------
# Add Stream
# -----------------------------
@app.route("/add", methods=["POST"])
def add_stream():
    name = request.form["name"]
    url = request.form["url"]
    group = request.form["group"]

    new_stream = Stream(name=name, url=url, group=group)
    db.session.add(new_stream)
    db.session.commit()

    return redirect("/")

# -----------------------------
# Delete Stream
# -----------------------------
@app.route("/delete/<int:id>")
def delete_stream(id):
    stream = Stream.query.get(id)
    if stream:
        db.session.delete(stream)
        db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
