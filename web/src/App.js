import React, {Component} from "react";
import './App.css';
import "bootstrap/dist/css/bootstrap.min.css";
import {Button, Card, Col, Container, Form, Row, Spinner} from "react-bootstrap";
import {ReturnChart} from "./ReturnChart";
import _ from 'lodash'


export default class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            loading: false,
            start: 2015,
            end: 2018,
            beta: 0.2,
            margin: 0.1,
            portfolio: null,
            jgindChartData: null,
            jcsevChartData: null,
        };
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange = (event) => {
        this.setState({[event.target.name]: Number(event.target.value), portfolio: null});
    };

    getInvestmentPortfolio = () => {
        const endpoint = `http://127.0.0.1:5000/invest/`;
        const query = {
            start: this.state.start,
            end: this.state.end,
            beta: this.state.beta,
            margin: this.state.margin,
        };
        const url = endpoint + this.encodeParameters(query);
        fetch(url, {
            method: "GET",
        })
            .then((response) => response.json())
            .then((response) => {
                this.setState({
                    portfolio: response.ip,
                });
            })
            .catch((err) => {
                console.log(err);
            });
    };

    processData = (index) => {
        if (this.state.portfolio == null) {
            return []
        }
        let data = []
        let annualReturns = this.state.portfolio[index]["annualReturns"]
        let benchmarkAnnualReturns = this.state.portfolio[index]["benchmarkAnnualReturns"]
        for (let i = this.state.start - this.state.start; i < this.state.end - this.state.start; i++) {
            data.push({
                Year: i + this.state.start,
                IP: (100 * annualReturns[i]).toFixed(2),
                Benchmark: (100 * benchmarkAnnualReturns[i]).toFixed(2)
            })
        }
        return data
    }


    encodeParameters = (params) => {
        let query = Object.keys(params)
            .map((k) => encodeURIComponent(k) + "=" + encodeURIComponent(params[k]))
            .join("&");
        return `?${query}`;
    };

    render() {
        return (
            <div className="App">
                <Container>
                    <Row>
                        <Col md={12}>
                            <h1 style={{fontSize: "6rem"}}>INVEST</h1>
                        </Col>
                    </Row>
                    <Row style={{textAlign: "left"}}>
                        <Col md={6} sm={12} style={{marginBottom: "1rem"}}>
                            <Card className={"card"}>
                                <Card.Body>
                                    <Card.Title>Control Panel</Card.Title>
                                    <Form>
                                        <Row>
                                            <Col>
                                                <Form.Group>
                                                    <Form.Label>Start</Form.Label>
                                                    <Form.Control name="start" as="select" onChange={this.handleChange}
                                                                  value={this.state.start}>
                                                        {_.range(2015, 2020).map((e) => {
                                                            return <option>{e}</option>
                                                        })}
                                                    </Form.Control>
                                                </Form.Group>
                                            </Col>
                                            <Col>
                                                <Form.Group>
                                                    <Form.Label>End</Form.Label>
                                                    <Form.Control name="end" as="select" onChange={this.handleChange}
                                                                  value={this.state.end}>
                                                        {_.range(2016, 2021).map((e) => {
                                                            return <option>{e}</option>
                                                        })}
                                                    </Form.Control>
                                                </Form.Group>
                                            </Col>
                                            <Col>
                                                <Form.Group>
                                                    <Form.Label>Beta</Form.Label>
                                                    <Form.Control name="beta" as="select" onChange={this.handleChange}
                                                                  value={this.state.beta}>
                                                        {_.range(0, 1.1, 0.1).map((e) => {
                                                            return <option>{e.toPrecision(1)}</option>
                                                        })}
                                                    </Form.Control>
                                                </Form.Group>
                                            </Col>
                                            <Col>
                                                <Form.Group>
                                                    <Form.Label>Margin</Form.Label>
                                                    <Form.Control name="margin" as="select" onChange={this.handleChange}
                                                                  value={this.state.margin}>
                                                        {_.range(0, 1.1, 0.1).map((e) => {
                                                            return <option>{e.toPrecision(1)}</option>
                                                        })}
                                                    </Form.Control>
                                                </Form.Group>
                                            </Col>
                                            <Col style={{margin: "20px 0 0 0"}}>
                                                <Button size="lg" variant="outline-secondary"
                                                        onClick={this.getInvestmentPortfolio}>Predict</Button>{' '}
                                            </Col>
                                        </Row>
                                    </Form>
                                </Card.Body>
                            </Card>
                        </Col>
                        <Col md={3} sm={12} style={{marginBottom: "1rem"}}>

                            <Card style={{height: "8.5rem"}} className={"card"}>
                                <Card.Body>
                                    <Row>
                                        <Col md={12}>
                                            <Card.Title>COGSPMS</Card.Title>
                                            <Card.Subtitle>&copy; 2021 University of Cape Town </Card.Subtitle>
                                            <Card.Text><br/>Insaaf Dhansay & Kialan Pillay</Card.Text>
                                        </Col>
                                    </Row>
                                </Card.Body>
                            </Card>
                        </Col>
                        <Col md={3} sm={12} style={{marginBottom: "1rem"}}>
                            <Card style={{height: "8.5rem"}} className={"card"}>
                                <Card.Body>
                                    <Row>
                                        <Col md={12}>
                                            <Card.Title>Acknowledgements</Card.Title>
                                            <Card.Text>This work is based on research partly funded by the National
                                                Research Foundation of South Africa </Card.Text>
                                        </Col>
                                    </Row>
                                </Card.Body>
                            </Card>
                        </Col>
                    </Row>
                    {this.state.portfolio ?
                        <div>
                            <Row style={{marginTop: "1rem", textAlign: "left"}}>
                                <Col md={3} sm={12} style={{margin: "0 0 1rem 0"}}>
                                    <Card className={"card"}>
                                        <Card.Body>
                                            <Card.Title>JGIND</Card.Title>
                                            <Card.Subtitle className="mb-2 text-muted">Investment
                                                Portfolio</Card.Subtitle>
                                            <Card.Subtitle
                                                className="mb-2 text-muted">{this.state.start} - {this.state.end}</Card.Subtitle>

                                            <table style={{border: "0"}}>
                                                <tbody>
                                                <tr>
                                                    <td style={{width: "95%"}}>Compound Return</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jgind"]["compoundReturn"] * 100).toFixed(2)}%</b>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style={{width: "95%"}}>Average Annual Return</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jgind"]["averageAnnualReturn"] * 100).toFixed(2)}%</b>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style={{width: "95%"}}>Treynor Ratio</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jgind"]["treynor"]).toFixed(2)}</b>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style={{width: "95%"}}>Sharpe Ratio</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jgind"]["sharpe"]).toFixed(2)}</b>
                                                    </td>
                                                </tr>
                                                </tbody>
                                            </table>

                                        </Card.Body>
                                    </Card>

                                </Col>
                                <Col md={3} sm={12} style={{marginBottom: "1rem"}}>
                                    <Card className={"card"}>
                                        <Card.Body>
                                            <Card.Title>JGIND</Card.Title>
                                            <Card.Subtitle className="mb-2 text-muted">Benchmark</Card.Subtitle>
                                            <Card.Subtitle
                                                className="mb-2 text-muted">{this.state.start} - {this.state.end}</Card.Subtitle>
                                            <table style={{border: "0"}}>
                                                <tbody>
                                                <tr>
                                                    <td style={{width: "95%"}}>Compound Return</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jgind"]["benchmarkCompoundReturn"] * 100).toFixed(2)}%</b>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style={{width: "95%"}}>Average Annual Return</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jgind"]["benchmarkAverageAnnualReturn"] * 100).toFixed(2)}%</b>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style={{width: "95%"}}>Treynor Ratio</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jgind"]["benchmarkTreynor"]).toFixed(2)}</b>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style={{width: "95%"}}>Sharpe Ratio</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jgind"]["benchmarkSharpe"]).toFixed(2)}</b>
                                                    </td>
                                                </tr>
                                                </tbody>
                                            </table>

                                        </Card.Body>
                                    </Card>
                                </Col>
                                <Col md={3} sm={12} style={{marginBottom: "1rem"}}>
                                    <Card className={"card"}>
                                        <Card.Body>
                                            <Card.Title>JCSEV</Card.Title>
                                            <Card.Subtitle className="mb-2 text-muted">Investment
                                                Portfolio</Card.Subtitle>
                                            <Card.Subtitle
                                                className="mb-2 text-muted">{this.state.start} - {this.state.end}</Card.Subtitle>
                                            <table style={{border: "0"}}>
                                                <tbody>
                                                <tr>
                                                    <td style={{width: "95%"}}>Compound Return</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jcsev"]["compoundReturn"] * 100).toFixed(2)}%</b>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style={{width: "95%"}}>Average Annual Return</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jcsev"]["averageAnnualReturn"] * 100).toFixed(2)}%</b>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style={{width: "95%"}}>Treynor Ratio</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jcsev"]["treynor"]).toFixed(2)}</b>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style={{width: "95%"}}>Sharpe Ratio</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jcsev"]["sharpe"]).toFixed(2)}</b>
                                                    </td>
                                                </tr>
                                                </tbody>
                                            </table>

                                        </Card.Body>
                                    </Card>
                                </Col>
                                <Col md={3} sm={12} style={{marginBottom: "1rem"}}>
                                    <Card className={"card"}>
                                        <Card.Body>
                                            <Card.Title>JCSEV</Card.Title>
                                            <Card.Subtitle className="mb-2 text-muted">Benchmark</Card.Subtitle>
                                            <Card.Subtitle
                                                className="mb-2 text-muted">{this.state.start} - {this.state.end}</Card.Subtitle>
                                            <table style={{border: "0"}}>
                                                <tbody>
                                                <tr>
                                                    <td style={{width: "95%"}}>Compound Return</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jcsev"]["benchmarkCompoundReturn"] * 100).toFixed(2)}%</b>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style={{width: "95%"}}>Average Annual Return</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jcsev"]["benchmarkAverageAnnualReturn"] * 100).toFixed(2)}%</b>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style={{width: "95%"}}>Treynor Ratio</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jcsev"]["benchmarkTreynor"]).toFixed(2)}</b>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style={{width: "95%"}}>Sharpe Ratio</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jcsev"]["benchmarkSharpe"]).toFixed(2)}</b>
                                                    </td>
                                                </tr>
                                                </tbody>
                                            </table>
                                        </Card.Body>
                                    </Card>
                                </Col>
                            </Row></div> : <Row style={{marginTop: "1rem", textAlign: "left"}}>
                            {this.state.loading ? <Spinner animation="border" role="status">
                                <span className="sr-only"></span>
                            </Spinner> : null}
                        </Row>
                    }
                    {this.state.portfolio ? <div>
                        <Row style={{marginTop: "1rem", textAlign: "left"}}>
                            <Col md={6} sm={12} style={{marginTop: "1rem"}}>
                                <Card className={"card"}>
                                    <Card.Body>
                                        <Card.Title>JGIND</Card.Title>
                                        <Card.Subtitle className="mb-2 text-muted">Annual Returns</Card.Subtitle>
                                        <ReturnChart data={this.processData("jgind")}/>
                                    </Card.Body>
                                </Card>

                            </Col>
                            <Col md={6} sm={12} style={{marginTop: "1rem"}}>
                                <Card className={"card"}>
                                    <Card.Body>
                                        <Card.Title>JCSEV</Card.Title>
                                        <Card.Subtitle className="mb-2 text-muted">Annual Returns</Card.Subtitle>
                                        <ReturnChart data={this.processData("jcsev")}/>
                                    </Card.Body>
                                </Card>
                            </Col>
                        </Row>
                    </div> : null}
                </Container>
            </div>
        );
    }
}
