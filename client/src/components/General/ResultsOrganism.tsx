import LineChart from "./LineChart.tsx";
import TableOfData from "./TableOfData.tsx";

type ResultsOrganismProps = {
    postgreTimes: number[],
    mongoTimes: number[],
}


export default function ResultsOrganism({postgreTimes, mongoTimes}: ResultsOrganismProps) {



    return (
        <div className="results-organism-div">
            <span>Results</span>
            <div className="tables-div">
                <TableOfData title={'Postgre times'} timesArray={postgreTimes}/>
                <TableOfData title={'Mongo times'} timesArray={mongoTimes}/>
            </div>
            <div className="charts-div">
                <LineChart title={'Postgre times'} timesArray={postgreTimes} chartColor={'blue'}/>
                <LineChart title={'Mongo times'} timesArray={mongoTimes} chartColor={'red'}/>
            </div>
        </div>
    )
}