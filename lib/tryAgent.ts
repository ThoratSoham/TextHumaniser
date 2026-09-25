import { simplify } from "./agents";

async function main() {
    const robot = "It is important to note that the utilization of the system commences prior to the finalization of the report.";
    console.log("BEFORE:", robot);
    const simple = await simplify(robot);
    console.log("AFTER:", simple);
}

main();