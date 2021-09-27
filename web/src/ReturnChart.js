import React from 'react';
import {Bar, BarChart, LabelList, Legend, ReferenceLine, ResponsiveContainer, XAxis, YAxis} from 'recharts';


export function ReturnChart(props) {
    return (
        <ResponsiveContainer width="90%" height={300}>
            <BarChart
                data={props.data}
                margin={{
                    top: 20,
                    right: 0,
                    left: 0,
                    bottom: 10,
                }}
            >
                <XAxis dataKey="Year"/>
                <YAxis label={{value: 'AR (%)', angle: -90, position: 'insideLeft', offset: 10}}
                       domain={[dataMin => Math.round(dataMin - 20), dataMax => Math.round(dataMax + 20)]}/>
                <Legend/>
                <ReferenceLine y={0} stroke="silver"/>
                <Bar dataKey="IP" fill="#327aff">
                    <LabelList dataKey="IP" position="top" fill={"black"} fontSize={"0.8rem"}/>
                </Bar>
                <Bar dataKey="Benchmark" fill="#ffa600">
                    <LabelList dataKey="Benchmark" position="top" fill={"black"} fontSize={"0.8rem"}/>
                </Bar>
            </BarChart>
        </ResponsiveContainer>
    );
}
