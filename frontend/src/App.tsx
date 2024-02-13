import "./App.css";
import styled from "styled-components";
import { SideNav } from "./components/LayoutComponents/SideNav";
import { LoadingWrapper } from "./components/LoadingWrapper";
import { useState } from "react";
import { DrawingBox } from "./components/LayoutComponents/DrawingBox";

function App() {
  const [isLoading, setLoading] = useState<boolean>(false);
  const [data, setData] = useState();

  return (
    <StyledApp>
      <div className="container">
        <div className="sideNav">
          <SideNav
            setLoader={(v) => setLoading(v)}
            onDataFetched={(data) => {
              setData(data);

              setLoading(false);
            }}
          />
        </div>
        <div className="drawingBoard">
          <LoadingWrapper isLoading={isLoading}>
            <DrawingBox data={data} />
          </LoadingWrapper>
        </div>
      </div>
    </StyledApp>
  );
}

const StyledApp = styled.main`
  .container {
    display: flex;
    justify-items: space;
  }

  .drawingBoard {
    flex: 1;
    width: 600px;
  }

  .sideNav {
    width: 400px;
    height: 100vh;
  }
`;

export default App;
