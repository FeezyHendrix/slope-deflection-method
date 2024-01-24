document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("numSpans").addEventListener("change", updateSpanDetails);
});

// Gather basic data
let numSupports = parseInt(document.getElementById("numSupports").value);
let numJoints = parseInt(document.getElementById("numJoints").value);
let numNodes = numSupports + numJoints;
let numSpans = numNodes - 1;
let length_of_beam = 0;
let settlementPositions = [];

// Initialize arrays for storing span and node data
let spans = [];
let nodes = [];

const P_C = "P_C"; // point load in center
const P_X = "P_X"; // Point load at distance 'a' from left end and 'b' from the right end
const P_C_2 = "P_C_2"; // Two equal point loads, spaced at 1/3 of the total length from each other
const P_C_3 = "P_C_3"; // Three equal point loads, spaced at 1/4 of the total length from each other
const UDL = "UDL"; // Uniformly distributed load over the whole length (UDL)
const UDL_2_R = "UDL/2_R"; // Uniformly distributed load over half of the span on the right side
const UDL_2_L = "UDL/2_L"; // Uniformly distributed load over half of the span on the left side
const VDL_R = "VDL_R"; // Variably distributed load, with highest point on the right end
const VDL_L = "VDL_L"; // Variably distributed load, with highest point on the left end
const VDL_C = "VDL_C"; // Variably distributed load, with highest point at the center

function updateSpanDetails() {
  let numSpans = document.getElementById("numSpans").value;
  let spanDetailsContainer = document.getElementById("spanDetails");
  spanDetailsContainer.innerHTML = "";

  for (let i = 1; i <= numSpans; i++) {
    let spanDiv = document.createElement("div");
    spanDiv.innerHTML = `
          <h3>Span ${i}</h3>
          <label for="spanLength${i}">Length of Span ${i}:</label>
          <input type="number" id="spanLength${i}" name="spanLength${i}" required><br>

          <label for="loadingCondition${i}">Loading Condition on Span ${i}:</label>
          <select type="text" id="loadingCondition${i}" name="loadingCondition${i}" onchange="updateLoadingCondition(${i})" required>
            <option value="none">None</option>
            <option value="P_C">Point load at center</option>
            <option value="P_X">Point load at distance 'a' from left end and 'b' from the right end </option>
            <option value="P_C_2">Two equal point loads, spaced at 1/3 of the total length from each other</option>
            <option value="P_C_3">Three equal point loads, spaced at 1/4 of the total length from each other</option>
            <option value="UDL">Uniformly distributed load over the whole length</option>
            <option value="UDL/2_R">Uniformly distributed load over half of the span on the right side </option>
            <option value="UDL/2_L">Uniformly distributed load over half of the span on the left side</option>
            <option value="VDL_R">Variably distributed load, with highest point on the right end</option>
            <option value="VDL_L">Variably distributed load, with highest point on the left end </option>
            <option value="VDL_C">Variably distributed load, with highest point at the center</option>
          </select>

          <div id="additionalInputs${i}"></div>
          <br>

          <label for="magnitudeOfLoad${i}">Magnitude of Load on Span ${i}:</label>
          <input type="number" id="magnitudeOfLoad${i}" name="magnitudeOfLoad${i}" required><br>
      `;
    spanDetailsContainer.appendChild(spanDiv);
  }
}

function updateLoadingCondition(spanIndex) {
  let selectedCondition = document.getElementById(`loadingCondition${spanIndex}`).value;
  let additionalInputsContainer = document.getElementById(`additionalInputs${spanIndex}`);
  additionalInputsContainer.innerHTML = "";

  if (selectedCondition === "P_X") {
    additionalInputsContainer.innerHTML = `
          <label for="spanALength${spanIndex}">Distance from point load to the left end joint (Span A Length):</label>
          <input type="number" id="spanALength${spanIndex}" name="spanALength${spanIndex}" required><br>
      `;
  }
}

document.getElementById("beamForm").addEventListener("submit", function (event) {
  event.preventDefault();
  // Populate spans array with user input
  for (let i = 0; i < numSpans; i++) {
    spans.push({
      spanLength: parseInt(document.getElementById(`spanLength${i + 1}`).value),
      load: parseInt(document.getElementById(`magnitudeOfLoad${i + 1}`).value),
      loadingCondition: document.getElementById(`loadingCondition${i + 1}`).value,
      // Add other properties as needed
    });
  }

  // Initialize nodes - Placeholder, further logic needed

  // calculate FEM
  spans.forEach((span, i) => {
    switch (span.loadingCondition) {
      case "P_C":
        span.rightFem = (span.load * span.spanLength) / 8;
        span.leftFem = -span.rightFem;
        break;

      case "P_X":
        // Assuming spanAValue is already set in span, otherwise, you need to set it here.
        let a = span.spanAValue;
        let b = span.spanLength - a;
        span.rightFem = (span.load * b * a * a) / (span.spanLength * span.spanLength);
        span.leftFem = (span.load * b * b * a) / (span.spanLength * span.spanLength);
        break;

      case "P_C_2":
        span.rightFem = (2 * span.load * span.spanLength) / 9;
        span.leftFem = -span.rightFem;
        break;

      case "P_C_3":
        span.rightFem = (15 * span.load * span.spanLength) / 48;
        span.leftFem = -span.rightFem;
        break;

      case "UDL":
        span.rightFem = (span.load * span.spanLength * span.spanLength) / 12;
        span.leftFem = -span.rightFem;
        break;

      case "UDL/2_R":
        span.rightFem = (11 * span.load * span.spanLength * span.spanLength) / 192;
        span.leftFem = -((5 * span.load * span.spanLength * span.spanLength) / 192);
        break;

      case "UDL/2_L":
        span.rightFem = (5 * span.load * span.spanLength * span.spanLength) / 192;
        span.leftFem = -((11 * span.load * span.spanLength * span.spanLength) / 192);
        break;

      case "VDL_R":
        span.rightFem = (span.load * span.spanLength * span.spanLength) / 20;
        span.leftFem = -((span.load * span.spanLength * span.spanLength) / 30);
        break;

      case "VDL_L":
        span.rightFem = (span.load * span.spanLength * span.spanLength) / 30;
        span.leftFem = -((span.load * span.spanLength * span.spanLength) / 20);
        break;

      case "VDL_C":
        span.rightFem = (5 * span.load * span.spanLength * span.spanLength) / 96;
        span.leftFem = -span.rightFem;
        break;

      case "none":
      default:
        span.rightFem = 0;
        span.leftFem = 0;
        console.log(`No loading on span ${i + 1}`);
    }
  });

  // Initialize the list of unknown end moments
  let listOfEndMoments = [];
  let leftEnd = "a";
  let rightEnd = "b";

  for (let i = 0; i < spans.length; i++) {
    spans[i].leftMoment = math.parse(`M${leftEnd}${rightEnd}`);
    spans[i].rightMoment = math.parse(`M${rightEnd}${leftEnd}`);
    leftEnd = String.fromCharCode(leftEnd.charCodeAt(0) + 1);
    rightEnd = String.fromCharCode(rightEnd.charCodeAt(0) + 1);
    listOfEndMoments.push(spans[i].leftMoment);
    listOfEndMoments.push(spans[i].rightMoment);
  }

  // Handle settlement on the beam
  let settlementOnBeam = document.getElementById("settlement").value;
  if (settlementOnBeam !== "yes") {
    console.log("No settlement on beam");
    nodes.forEach((node) => (node.settlement = 0));
  } else {
    let position = prompt("Input the first settlement position: ");
    while (position !== "") {
      settlementPositions.push(parseInt(position));
      position = prompt("Input the next settlement position (leave empty to finish): ");
    }
    nodes.forEach((node, index) => {
      if (settlementPositions.includes(index)) {
        node.settlement = parseInt(prompt(`Value of settlement at position ${index}?: `));
      } else {
        node.settlement = 0;
      }
    });
  }

  // Calculating cord rotation for each span
  spans.forEach((span, i) => {
    span.cordRotation = (nodes[i + 1].settlement - nodes[i].settlement) / span.spanLength;
  });

  // Check if the first and last nodes are fixed
  let firstNodeFixed = document.getElementById("firstNodeFixed");
  let lastNodeFixed = document.getElementById("lastNodeFixed");

  // Express the slope deflection equations for each span
  let listOfSlopeDeflectionEquations = [];

  spans.forEach((span, i) => {
    if (i === 0 && firstNodeFixed === "no") {
      span.leftSlopeDeflectionEquation = { equation: "0 = " + span.leftMoment.toString() };
      span.rightSlopeDeflectionEquation = {
        equation: `3 * (Theta_${i + 1} - ${span.cordRotation}) / ${span.spanLength} + ${span.rightFem} = ${
          span.rightMoment
        }`,
      };
    } else if (i === spans.length - 1 && lastNodeFixed === "no") {
      span.leftSlopeDeflectionEquation = {
        equation: `3 * (Theta_${i} - ${span.cordRotation}) / ${span.spanLength} + ${span.leftFem} = ${span.leftMoment}`,
      };
      span.rightSlopeDeflectionEquation = { equation: "0 = " + span.rightMoment.toString() };
    } else {
      span.leftSlopeDeflectionEquation = {
        equation: `2 * (2 * Theta_${i} + Theta_${i + 1} - 3 * ${span.cordRotation}) / ${span.spanLength} + ${
          span.leftFem
        } = ${span.leftMoment}`,
      };
      span.rightSlopeDeflectionEquation = {
        equation: `2 * (2 * Theta_${i + 1} + Theta_${i} - 3 * ${span.cordRotation}) / ${span.spanLength} + ${
          span.rightFem
        } = ${span.rightMoment}`,
      };
    }
    listOfSlopeDeflectionEquations.push(span.leftSlopeDeflectionEquation);
    listOfSlopeDeflectionEquations.push(span.rightSlopeDeflectionEquation);
  });

  let listOfEquilibriumEquations = [];
nodes.forEach((node, i) => {
    if (i !== 0 && i !== nodes.length - 1) {
        node.equilibriumEquation = math.parse(`${spans[i - 1].rightMoment} + ${spans[i].leftMoment} = 0`);
    } else {
        node.equilibriumEquation = math.parse("0 = 0");
    }
    listOfEquilibriumEquations.push(node.equilibriumEquation);
});

// Assuming listOfSlopeDeflectionEquations, listOfEndMoments, listOfUnknownAngularDisplacements are defined
let equations = listOfSlopeDeflectionEquations.concat(listOfEquilibriumEquations);
let unknowns = listOfEndMoments.concat(listOfUnknownAngularDisplacements);

// Solving equations - This is a simplistic approach and might not work for complex systems
let solutions = {};
unknowns.forEach(unknown => {
    // Simplify the process by just trying to solve each equation numerically
    // This is a limitation as compared to sympy's symbolic solving
    equations.forEach(eq => {
        try {
            let solution = math.solve(eq, unknown);
            if (solution) {
                solutions[unknown] = solution;
            }
        } catch (error) {
            console.log("Error solving equation:", error);
        }
    });
});

console.log(equations);
console.log(solutions);
// Displaying specific solutions would depend on how the unknowns are defined

});
