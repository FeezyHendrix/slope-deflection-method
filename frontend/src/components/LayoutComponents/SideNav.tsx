/* eslint-disable @typescript-eslint/no-explicit-any */
import styled from "styled-components";
import { useForm } from "@mantine/form";
import { loadingCondition } from "../../utils/contants";
import deleteIcon from "../../assets/delete.png";
import { useState } from "react";

interface SpanData {
  span_length: number;
  load: number;
  loading_condition: loadingCondition;
}

interface SideNavInterface {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  onDataFetched: (data: any) => void;
  setLoader: (value: boolean) => void;
}

export function SideNav({ setLoader, onDataFetched }: SideNavInterface) {
  const [isButtonLoading, setIsButtonLoading] = useState<boolean>(false);
  const form = useForm({
    initialValues: {
      number_of_supports: 0,
      number_of_internal_joints: 0,
      span_data: [] as SpanData[],
      settlement_positions: [] as number[],
      settlement_values: [] as number[],
      settlement_on_beam: "no",
      first_node_fixed: "yes",
      last_node_fixed: "no",
    },
  });

  const onAddSpanClick = () => {
    form.setValues((prev) => ({
      ...prev,
      span_data: [
        ...(prev.span_data || []), // Ensure it's always an array
        { load: 0, span_length: 0, loading_condition: "P_C" },
      ],
    }));
  };

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const onSubmitClick = async (values: any) => {
    setLoader(true);
    setIsButtonLoading(true);
    try {
      console.log(values);
      const payload = {
        number_of_supports: !isNaN(parseInt(values.number_of_supports, 10)) ? parseInt(values.number_of_supports) : 0,
        number_of_internal_joints: !isNaN(parseInt(values.number_of_internal_joints, 10)) ? parseInt(values.number_of_internal_joints) : 0,
        span_data: values.span_data.map((_: any) => ({ load: parseInt(_.load), 'span_length': parseInt(_.span_length), 'loading_condition': _.loading_condition })),
        first_node_fixed: values.first_node_fixed,
        last_node_fixed: values.last_node_fixed,
        settlement_on_beam: values.settlement_on_beam,
        settlement_on_values: (values.settlement_on_values || []).map((_: any) => parseInt(_)),
        settlement_positions: (values.settlement_positions || []).map((_: any) => parseInt(_)),
      }
      const response = await fetch("http://127.0.0.1:6900/calculate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      console.log(data);
      onDataFetched(data);
      setIsButtonLoading(false);
    } catch (e) {
      console.log(e);
      setIsButtonLoading(false);
    }
  };

  return (
    <StyledNav>
      <form onSubmit={form.onSubmit((values) => onSubmitClick(values))}>
        <h2>Beam Analysis Calculator</h2>
        <div className="formContainer">
          <label>Number of Supports:</label>
          <input
            {...form.getInputProps("number_of_supports")}
            type="number"
            id="numSupports"
            name="numSupports"
            required
          />
        </div>

        <br />
        <div className="formContainer">
          <label>Number of Internal Joints:</label>
          <input
            {...form.getInputProps("number_of_internal_joints")}
            type="number"
            id="numJoints"
            name="numJoints"
            required
          />
        </div>
        <br />
        <div className="flex">
          <h4>Beam Spans</h4>
          <button type="button" className="span__button" onClick={onAddSpanClick}>
            Add Span
          </button>
        </div>
        <div className="spanDetails">
          <table>
            <thead>
              <tr>
                <th className="tableHead">No</th>
                <th className="tableHead">Span Length</th>
                <th className="tableHead">Loading Condition on Span</th>
                <th className="tableHead">Magnitude</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {form.values.span_data.map((v, i) => {
                return (
                  <tr key={i}>
                    <td>{i + 1}</td>
                    <td>
                      <input
                        placeholder="length of span"
                        onChange={(v) => {
                          form.setFieldValue(`span_data.${i}.span_length`, v.target.value);
                        }}
                        value={v.span_length}
                        type="number"
                      />
                    </td>
                    <td>
                      <select
                        value={v.loading_condition}
                        onChange={(v) => {
                          form.setFieldValue(`span_data.${i}.loading_condition`, v.target.value);
                        }}
                      >
                        <option value="none">None</option>
                        <option value="P_C">Point load at center</option>
                        <option value="P_X">
                          Point load at distance 'a' from left end and 'b' from the right end{" "}
                        </option>
                        <option value="P_C_2">
                          Two equal point loads, spaced at 1/3 of the total length from each other
                        </option>
                        <option value="P_C_3">
                          Three equal point loads, spaced at 1/4 of the total length from each other
                        </option>
                        <option value="UDL">Uniformly distributed load over the whole length</option>
                        <option value="UDL/2_R">
                          Uniformly distributed load over half of the span on the right side{" "}
                        </option>
                        <option value="UDL/2_L">
                          Uniformly distributed load over half of the span on the left side
                        </option>
                        <option value="VDL_R">Variably distributed load, with highest point on the right end</option>
                        <option value="VDL_L">Variably distributed load, with highest point on the left end </option>
                        <option value="VDL_C">Variably distributed load, with highest point at the center</option>
                      </select>
                    </td>
                    <td>
                      <input
                        value={v.load}
                        type="number"
                        onChange={(v) => {
                          form.setFieldValue(`span_data.${i}.load`, v.target.value);
                        }}
                      />
                    </td>
                    <td>
                      <img
                        src={deleteIcon}
                        className="deleteIcon"
                        onClick={() => form.removeListItem("span_data", i)}
                      />
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
          <br />
          <div className="formContainer">
            <label>Is First Node Fixed</label>
            <select {...form.getInputProps("first_node_fixed")}>
              <option value="yes">Yes</option>
              <option value="no">No</option>
            </select>
          </div>
          <br />
          <div className="formContainer">
            <label>Is Last Node Fixed</label>
            <select {...form.getInputProps("last_node_fixed")}>
              <option value="yes">Yes</option>
              <option value="no">No</option>
            </select>
          </div>
        </div>
        <br />
        <button className="submit__button" type="submit">
          Solve
        </button>
      </form>
    </StyledNav>
  );
}

const StyledNav = styled.div`
  table {
    border-collapse: separate;
    border-spacing: 10px;
  }
  input,
  select {
    border: 1px solid black;
    width: 100%;
    font-size: 14px;
    height: 30px;
    outline: none;
    color: #000;
    text-indent: 15px;
    line-height: 24px;
    background-color: #fff;
  }

  .deleteIcon {
    height: 15px;
    width: 15px;
    object-fit: contain;
    cursor: pointer;
  }

  .tableHead {
    font-size: 10px;
  }

  .formContainer {
    label {
      text-align: left;
      display: block;
      font-size: 12px;
    }
  }

  .flex {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .span__button {
    background-color: #0099ff;
    border: none;
    font-size: 12px;
    padding: 10px 20px;
    cursor: pointer;
  }

  .submit__button {
    background-color: #0099ff;
    width: 100%;
    height: 40px;
    font-size: 14px;
    border: none;
    cursor: pointer;
  }
`;
