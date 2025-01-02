import TableOfData from "./TableOfData.tsx";
import {useEffect, useState} from "react";
import ScatterChart from "./ScatterChart.tsx";

type ResultsOrganismProps = {
    postgreTimes: number[],
    mongoTimes: number[],
}


export default function ResultsOrganism({postgreTimes, mongoTimes}: ResultsOrganismProps) {

    const [postgreAverageTime, setPostgreAverageTime] = useState<number>(0)
    const [mongoAverageTime, setMongoAverageTime] = useState<number>(0)

    const calculateAverageTimes = () => {
        let postgreAvg = 0;
        let mongoAvg = 0;

        for (let item of postgreTimes) {
            postgreAvg += item;
        }

        for (let item of mongoTimes) {
            mongoAvg += item;
        }

        postgreAvg = postgreAvg / postgreTimes.length;
        mongoAvg = mongoAvg / mongoTimes.length;

        setPostgreAverageTime(postgreAvg);
        setMongoAverageTime(mongoAvg);
    }

    useEffect(()=>{
        calculateAverageTimes();
    }, [postgreTimes, mongoTimes])

    return (
        <div className="results-organism-div">
            <span>Results</span>
            <div className="tables-div">
                <TableOfData title={'Postgre times'} timesArray={postgreTimes}/>
                <TableOfData title={'Mongo times'} timesArray={mongoTimes}/>
            </div>
            <div className="charts-div">
                <ScatterChart title={'Postgre times'} timesArray={postgreTimes} chartColor={'blue'}/>
                <ScatterChart title={'Mongo times'} timesArray={mongoTimes} chartColor={'red'}/>
            </div>
            <div className="tables-div">
                <span>Average time: {postgreAverageTime.toFixed(3)}</span>
                <span>Average time: {mongoAverageTime.toFixed(3)}</span>
            </div>
        </div>
    )
}