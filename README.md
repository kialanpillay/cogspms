# COGSPMS

*An Intelligent System for Automated Portfolio Management using Graph Neural Networks and Semantic Bayesian Networks*

## Project Information

### Team

| Member          | Student Number|
| -------------   |-------------  |
| Insaaf Dhansay  | DHNINS001     |
| Kialan Pillay   | PLLKIA010     |

### Supervisor

| Staff Member              | Department           |
| -------------             |-------------         |
| A/Prof Deshendran Moodley | Computer Science     |

## Installation

```
source ./venv/bin/activate
pip3 install -Ur requirements.txt
```

## Web Console

```
python3 wsgi.py
cd web && npm install && npm start
```

## Experiments

### Graph Neural Networks

Single-Step Forecasting w/ Baseline

```
python3 gnn_main.py --model GWN --window_size 30 --horizon 1 --baseline True
python3 gnn_main.py --model GWN --window_size 60 --horizon 1 --baseline True
python3 gnn_main.py --model GWN --window_size 120 --horizon 1 --baseline True
```

Multi-Step Forecasting w/ Baseline

```
python3 gnn_main.py --model StemGNN --window_size 20 --horizon 20 --baseline True
python3 gnn_main.py --model GWN --window_size 20 --horizon 20 --baseline True
python3 gnn_main.py --model MTGNN --window_size 20 --horizon 20 --baseline True
```

Multi-Step Forecasting w/ Correlation Matrix

```
python3 gnn_main.py --model GWN --window_size 20 --horizon 10 --adj_data True --apt_only False --random_adj False
python3 gnn_main.py --model MTGNN --window_size 20 --horizon 10 --adj_data True --build_adj False
```

Inference

```
python3 gnn_main.py --model GWN --window_size 20 --horizon 10 --baseline True --train False
```

Network Analysis

```
python3 gnn/analysis/main.py --network True --n 5 --hierarchical False --plot True
```

### Semantic Bayesian Networks

INVEST Base

```
python3 app.py --beta 0.2
python3 app.py --beta 0.6
python3 app.py --beta 1
```

INVEST Ablation Study

```
python3 app.py --beta 0.2 --ablation True --network v
python3 app.py --beta 0.2 --ablation True --network q
```

INVEST w/ Noise

```
python3 app.py --beta 0.2 --noise True
```

INVEST w/ Systematic Risk Extension

```
python3 app.py --beta 0.2 --extension True
python3 app.py --beta 1 --extension True
```

INVEST + GNN

```
python3 app.py --beta 0.2 --gnn True
```