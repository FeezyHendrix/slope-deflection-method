import React from "react";
import { Audio } from "react-loader-spinner";
import styled from "styled-components";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const LoadingWrapper = ({ isLoading, children }: any) => {
  return (
    <StyledLoadingWrapper>
      {isLoading ? (
        <div className="center">
          <Audio
            height="50"
            width="50"
            color="#0099ff"
            ariaLabel="audio-loading"
            wrapperStyle={{}}
            wrapperClass="loader-class"
            visible={true}
          ></Audio>
        </div>
      ) : (
        children
      )}
    </StyledLoadingWrapper>
  );
};

const StyledLoadingWrapper = styled.div`
  .center {
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
  }
`;
