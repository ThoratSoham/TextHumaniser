import { analyzeText } from "./analyze.js";
import { applyRuleImprovements } from "./rules";

const robotText =
  "It is important to note that we do not utilize the system prior to approval. " +
  "In conclusion, the report was approved, and the team was happy.";

const report = analyzeText(robotText);
console.log(report);
console.log("BEFORE:", robotText);
console.log("AFTER:", applyRuleImprovements(robotText));