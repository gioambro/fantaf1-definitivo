from flask import Flask, request, jsonify

app = Flask(__name__)

# Funzione per calcolare i punti di un pilota
def calc_pilot_points(p):
    pts = 0.0

# Punti base gara (prime 10 posizioni)
base_points = [25,18,15,12,10,8,6,4,2,1]
pos = p.get("position_gp")
if pos and 1 <= pos <= 10:
pts += base_points[pos-1]

# Bonus
if p.get("pole"): pts += 2
if p.get("fastest_lap"): pts += 1
if p.get("driver_of_the_day"): pts += 1
if p.get("fastest_pitstop"): pts += 2
if p.get("from_back_and_points"): pts += 2
pts += 0.5 * p.get("positions_gained", 0)
if p.get("win_gp"): pts += 3
if p.get("podium_gp"): pts += 2

# Malus
if p.get("disqualified"): pts -= 5
if p.get("dnf"): pts -= 3
sec = p.get("penalty_seconds", 0)
if sec >= 6: pts -= 4
elif 0 < sec <= 5: pts -= 3
if p.get("last_in_race") and not p.get("dnf"): pts -= 2
if p.get("no_q1"): pts -= 1
if not p.get("dnf"): pts -= 0.5 * p.get("positions_lost", 0)

return pts

# API per calcolare i punti
@app.route("/calculate", methods=["POST"])
def calculate():
data = request.get_json()
players = data.get("players", [])
results = {}
for player in players:
total = sum(calc_pilot_points(p) for p in player.get("pilots", []))
results[player["name"]] = {"total": total}
return jsonify(results)

if __name__ == "__main__":
app.run(host="0.0.0.0", port=5000)
