from flask import Flask, request, jsonify
import statcalc as sc
import simulator as sim

app = Flask(__name__)

@app.route('/stat', methods=['POST'])
def stat_data():
    data = request.json
    statobj = sc.StatCalc(data["eq"], data["unb"], data["data"], data["lb"], data["ub"], data["y"])
    # Process the received data
    print(f"Received data: {data}")
    simdata = statobj.send()
    response_data = {
        "stats": simdata,
    }
    return jsonify(response_data)

@app.route('/sim', methods=['POST'])
def sim_data():
    data = request.json
    simobj = sim.Simulator()
    #simobj = sim.Simulator(data["har"], data["wave"], data["t"], data["nrg"], data["op"])
    # Process the received data
    simulator = simobj.create_simulator(data["sim"], data["args"])
    print(f"Received data: {data}")
    sympy_plot = simulator.send()

    response_data = {
        "plot": sympy_plot
    }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
