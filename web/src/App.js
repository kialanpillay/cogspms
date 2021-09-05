import React, {Component} from "react";
import './App.css';
import "bootstrap/dist/css/bootstrap.min.css";
import {Badge, Button, Card, Col, Container, Form, Row, Spinner} from "react-bootstrap";
import {ReturnChart} from "./ReturnChart";
import _ from 'lodash'
import Switch from "@material-ui/core/Switch";
import { withStyles } from "@material-ui/core/styles";
import FormControlLabel from "@material-ui/core/FormControlLabel";
const IOSSwitch = withStyles((theme) => ({
  root: {
    width: 42,
    height: 26,
    padding: 0,
    margin: theme.spacing(1),
  },
  switchBase: {
    padding: 1,
    "&$checked": {
      transform: "translateX(16px)",
      color: theme.palette.common.white,
      "& + $track": {
        backgroundColor: "#52d869",
        opacity: 1,
        border: "none",
      },
    },
    "&$focusVisible $thumb": {
      color: "#52d869",
      border: "6px solid #fff",
    },
  },
  thumb: {
    width: 24,
    height: 24,
  },
  track: {
    borderRadius: 26 / 2,
    border: `1px solid ${theme.palette.grey[400]}`,
    backgroundColor: theme.palette.grey[50],
    opacity: 1,
    transition: theme.transitions.create(["background-color", "border"]),
  },
  checked: {},
  focusVisible: {},
}))(({ classes, ...props }) => {
  return (
    <Switch
      focusVisibleClassName={classes.focusVisible}
      disableRipple
      classes={{
        root: classes.root,
        switchBase: classes.switchBase,
        thumb: classes.thumb,
        track: classes.track,
        checked: classes.checked,
      }}
      {...props}
    />
  );
});

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
            extension: false,
            gnn:false,
            value:false,
            quality:false,
        };
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange = (event) => {
        this.setState({[event.target.name]: Number(event.target.value), portfolio: null});
    };

     handleSwitch = (event) => {
    this.setState({ [event.target.name]: !this.state.name,portfolio: null });
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
        this.setState({loading: true, portfolio: null})
        fetch(url, {
            method: "GET",
        })
            .then((response) => response.json())
            .then((response) => {
                this.setState({
                    loading: false,
                    portfolio: response.portfolio
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
        let annualReturns = this.state.portfolio[index]["ip"]["annualReturns"]
        let benchmarkAnnualReturns = this.state.portfolio[index]["benchmark"]["annualReturns"]
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
                        <Col xl={12} lg={12} md={12}>
                            <h1 style={{fontSize: "6rem"}}>INVE$T</h1>
                        </Col>
                    </Row>
                    <Row style={{textAlign: "left"}}>
                        <Col xl={6} lg={6} md={12} sm={12} style={{marginBottom: "1rem"}}>
                            <Card className={"card"}>
                                <Card.Body>
                                    <Card.Title>Control Panel</Card.Title>
                                    <Form>
                                        <Row>
                                            <Col lg={2} md={6} xs={6}>
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
                                            <Col lg={2} md={6} xs={6}>
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
                                            <Col lg={2} md={6} xs={6}>
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
                                            <Col lg={2} md={6} xs={6}>
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
                                                    <FormControlLabel
                                                     control={
                                                        <IOSSwitch
                                                            checked={this.state.extension}
                                                            onChange={this.handleSwitch}
                                                            name="extension"
                                                        />
                                                        }
                                                    />
                                            </Col>
                                            <Col style={{margin: "20px 0 0 0"}}>
                                                <Button size="lg" variant="outline-secondary"
                                                        style={{width: "100%", height: "100%"}}
                                                        onClick={this.getInvestmentPortfolio}>{this.state.loading ?
                                                    <Spinner animation="border" role="status">
                                                        <span className="sr-only"/>
                                                    </Spinner> : "Predict"}</Button>{' '}
                                            </Col>
                                        </Row>
                                    </Form>
                                </Card.Body>
                            </Card>
                        </Col>
                        <Col xl={3} lg={6} md={12} sm={12} style={{marginBottom: "1rem"}}>

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
                        <Col xl={3} lg={12} md={12} sm={12} style={{marginBottom: "1rem"}}>
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
                                <Col xl={3} lg={6} md={12} sm={12} style={{margin: "0 0 1rem 0"}}>
                                    <Card className={"card"}>
                                        <Card.Body>
                                            <Card.Title>JGIND</Card.Title>
                                            <Card.Subtitle className="mb-2 text-muted">
                                                <Badge style={{backgroundColor: "#bc5090"}}>Investment
                                                    Portfolio</Badge></Card.Subtitle>
                                            <Card.Subtitle
                                                className="mb-2 text-muted">{this.state.start} - {this.state.end}</Card.Subtitle>

                                            <table style={{border: "0"}}>
                                                <tbody>
                                                <tr>
                                                    <td style={{width: "95%"}}>Compound Return</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jgind"]["ip"]["compoundReturn"] * 100).toFixed(2)}%</b>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style={{width: "95%"}}>Average Annual Return</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jgind"]["ip"]["averageAnnualReturn"] * 100).toFixed(2)}%</b>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style={{width: "95%"}}>Treynor Ratio</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jgind"]["ip"]["treynor"]).toFixed(2)}</b>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style={{width: "95%"}}>Sharpe Ratio</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jgind"]["ip"]["sharpe"]).toFixed(2)}</b>
                                                    </td>
                                                </tr>
                                                </tbody>
                                            </table>

                                        </Card.Body>
                                    </Card>

                                </Col>
                                <Col xl={3} lg={6} md={12} sm={12} style={{marginBottom: "1rem"}}>
                                    <Card className={"card"}>
                                        <Card.Body>
                                            <Card.Title>JGIND</Card.Title>
                                            <Card.Subtitle className="mb-2 text-muted">
                                                <Badge
                                                    style={{backgroundColor: "#ffa600"}}>Benchmark</Badge></Card.Subtitle>
                                            <Card.Subtitle
                                                className="mb-2 text-muted">{this.state.start} - {this.state.end}</Card.Subtitle>
                                            <table style={{border: "0"}}>
                                                <tbody>
                                                <tr>
                                                    <td style={{width: "95%"}}>Compound Return</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jgind"]["benchmark"]["compoundReturn"] * 100).toFixed(2)}%</b>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style={{width: "95%"}}>Average Annual Return</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jgind"]["benchmark"]["averageAnnualReturn"] * 100).toFixed(2)}%</b>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style={{width: "95%"}}>Treynor Ratio</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jgind"]["benchmark"]["treynor"]).toFixed(2)}</b>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style={{width: "95%"}}>Sharpe Ratio</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jgind"]["benchmark"]["sharpe"]).toFixed(2)}</b>
                                                    </td>
                                                </tr>
                                                </tbody>
                                            </table>

                                        </Card.Body>
                                    </Card>
                                </Col>
                                <Col xl={3} lg={6} md={12} sm={12} style={{marginBottom: "1rem"}}>
                                    <Card className={"card"}>
                                        <Card.Body>
                                            <Card.Title>JCSEV</Card.Title>
                                            <Card.Subtitle className="mb-2 text-muted">
                                                <Badge style={{backgroundColor: "#bc5090"}}>Investment
                                                    Portfolio</Badge></Card.Subtitle>
                                            <Card.Subtitle
                                                className="mb-2 text-muted">{this.state.start} - {this.state.end}</Card.Subtitle>
                                            <table style={{border: "0"}}>
                                                <tbody>
                                                <tr>
                                                    <td style={{width: "95%"}}>Compound Return</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jcsev"]["ip"]["compoundReturn"] * 100).toFixed(2)}%</b>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style={{width: "95%"}}>Average Annual Return</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jcsev"]["ip"]["averageAnnualReturn"] * 100).toFixed(2)}%</b>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style={{width: "95%"}}>Treynor Ratio</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jcsev"]["ip"]["treynor"]).toFixed(2)}</b>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style={{width: "95%"}}>Sharpe Ratio</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jcsev"]["ip"]["sharpe"]).toFixed(2)}</b>
                                                    </td>
                                                </tr>
                                                </tbody>
                                            </table>

                                        </Card.Body>
                                    </Card>
                                </Col>
                                <Col xl={3} lg={6} md={12} sm={12} style={{marginBottom: "1rem"}}>
                                    <Card className={"card"}>
                                        <Card.Body>
                                            <Card.Title>JCSEV</Card.Title>
                                            <Card.Subtitle className="mb-2 text-muted">
                                                <Badge
                                                    style={{backgroundColor: "#ffa600"}}>Benchmark</Badge></Card.Subtitle>
                                            <Card.Subtitle
                                                className="mb-2 text-muted">{this.state.start} - {this.state.end}</Card.Subtitle>
                                            <table style={{border: "0"}}>
                                                <tbody>
                                                <tr>
                                                    <td style={{width: "95%"}}>Compound Return</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jcsev"]["benchmark"]["compoundReturn"] * 100).toFixed(2)}%</b>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style={{width: "95%"}}>Average Annual Return</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jcsev"]["benchmark"]["averageAnnualReturn"] * 100).toFixed(2)}%</b>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style={{width: "95%"}}>Treynor Ratio</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jcsev"]["benchmark"]["treynor"]).toFixed(2)}</b>
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style={{width: "95%"}}>Sharpe Ratio</td>
                                                    <td style={{textAlign: "right"}}>
                                                        <b>{(this.state.portfolio["jcsev"]["benchmark"]["sharpe"]).toFixed(2)}</b>
                                                    </td>
                                                </tr>
                                                </tbody>
                                            </table>
                                        </Card.Body>
                                    </Card>
                                </Col>
                            </Row></div> : null}
                    {this.state.portfolio ? <div>
                        <Row style={{marginTop: "1rem", textAlign: "left"}}>
                            <Col xl={6} lg={6} md={12} sm={12} style={{marginBottom: "1rem"}}>
                                <Card className={"card"}>
                                    <Card.Body>
                                        <Card.Title>JGIND</Card.Title>
                                        <Card.Subtitle className="mb-2 text-muted">Annual Returns</Card.Subtitle>
                                        <ReturnChart data={this.processData("jgind")}/>
                                    </Card.Body>
                                </Card>

                            </Col>
                            <Col xl={6} lg={6} md={12} sm={12} style={{marginBottom: "1rem"}}>
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
