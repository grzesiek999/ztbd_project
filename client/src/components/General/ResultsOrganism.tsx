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
            <span>Wyniki</span>
            <div className="tables-div">
                <TableOfData title={'Tabela czasow dla PostgreSQL'} timesArray={postgreTimes}/>
                <TableOfData title={'Tabela czasow dla MongoDB'} timesArray={mongoTimes}/>
            </div>
            <div className="charts-div">
                <ScatterChart title={'Wykres czasow dla PostgreSQL'} timesArray={postgreTimes} chartColor={'blue'}/>
                <ScatterChart title={'Wykres czasow dla MongoDB'} timesArray={mongoTimes} chartColor={'red'}/>
            </div>
            <div className="tables-div">
                <span>Sredni czas (ms): {postgreAverageTime.toFixed(3)}</span>
                <span>Sredni czas (ms): {mongoAverageTime.toFixed(3)}</span>
            </div>
        </div>
    )
}