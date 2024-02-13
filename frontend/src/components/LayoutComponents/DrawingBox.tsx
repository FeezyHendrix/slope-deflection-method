/* eslint-disable @typescript-eslint/no-explicit-any */
import { useEffect, useState } from "react";
import styled from "styled-components";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Area, ReferenceLine } from "recharts";

interface DrawingBoxInterface {
  data: any;
}

export const DrawingBox = ({ data }: DrawingBoxInterface) => {
  const [shearForcesChartValue, setShearForceChartValue] = useState<null | { name: string; ShearForce: any }[]>(null);

  useEffect(() => {
    if (data && data.shear_forces !== undefined) {
      const payload = data.shear_forces.map((value: string, index: any) => ({
        name: `Point ${index}`,
        ShearForce: parseFloat(value),
      }));

      setShearForceChartValue(payload);
    }
  }, [data]);
  return (
    <StyledDrawingBox>
      {data !== undefined && (
        <div className="momentDiv">
          <h4>Fixed End Moments</h4>
          <table>
            <thead>
              <tr>
                {data["equationSolution"] !== undefined &&
                  Object.entries(data.equationSolution).map(([key]) => <td key={key}>{key}</td>)}
              </tr>
            </thead>
            <tbody>
              <tr>
                {data["equationSolution"] !== undefined &&
                  Object.entries(data.equationSolution).map(([key, value]) => (
                    <td key={key}>{Number(value as any).toFixed(2)}</td>
                  ))}
              </tr>
            </tbody>
          </table>
          <br />
          <h4>Shear Force Diagram</h4>
          <div className="shearForce">
            {shearForcesChartValue !== null && (
              <LineChart
                width={700}
                height={400}
                data={shearForcesChartValue}
                margin={{
                  top: 5,
                  right: 30,
                  left: 20,
                  bottom: 5,
                }}
              >
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="linear" dataKey="ShearForce" stroke="#8884d8" activeDot={{ r: 8 }} />
                <ReferenceLine y={0} stroke="black" strokeDasharray="5 5" />

                <Area type="linear" dataKey="ShearForce" stroke="#8884d8" fill="#8884d8" fillOpacity={0.3} />
              </LineChart>
            )}
          </div>
        </div>
      )}
    </StyledDrawingBox>
  );
};

const StyledDrawingBox = styled.div`
  margin-left: 40px;
  .momentDiv {
    table {
      width: 100%;
    }
    thead {
      td {
        background-color: black;
        color: white;
      }
    }
    td {
      font-size: 10px;
      text-align: center;
    }
  }
`;
