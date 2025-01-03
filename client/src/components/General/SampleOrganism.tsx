import {SyntheticEvent, useEffect, useState} from "react";
import ResultsOrganism from "./ResultsOrganism.tsx";


type SampleOrganismProps = {
    path: string
    httpMethod: string;
}

export default function SampleOrganism({path, httpMethod}: SampleOrganismProps) {

    const [samples_count, set_samples_count] = useState<number>(0);
    const [rows_count, set_rows_count] = useState<number>(0);
    const [postgreTimes, setPostgreTimes] = useState<number[]>([]);
    const [mongoTimes, setMongoTimes] = useState<number[]>([]);
    const [sendData, setSendData] = useState<{}>({});

    const useQuery = async (e: SyntheticEvent) => {
        e.preventDefault();

        const response = await fetch(path, {
            method: httpMethod,
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(sendData)
        });
        if (response.ok) {
            const data = await response.json();

            if (data.mongo_execution_times && Array.isArray(data.mongo_execution_times)) {
                setMongoTimes(data.mongo_execution_times);
            } else { setMongoTimes([]); }

            if (data.postgres_execution_times && Array.isArray(data.postgres_execution_times)) {
                setPostgreTimes(data.postgres_execution_times);
            } else { setPostgreTimes([]); }

        } else { console.log(response.status, response.statusText); }
    }


    useEffect(()=>{
        const data: Record<string, number | null> = {};

        if (samples_count !== null) {
            data.samples_count = samples_count;
        }
        if (rows_count !== null && rows_count !== 0) {
            data.rows_count = rows_count;
        }

        setSendData(data);
    },[samples_count, rows_count])

    const handleIdListSize = (e: React.ChangeEvent<HTMLInputElement>) => {
        if(e.target.value === '') { set_rows_count(0); }
        else {
            const str_numb = e.target.value;
            set_rows_count(parseInt(str_numb));
        }
    }

    const handleSampleNumber = (e: React.ChangeEvent<HTMLInputElement>) => {
        if(e.target.value === '') { set_samples_count(0); }
        else {
            const str_numb = e.target.value;
            set_samples_count(parseInt(str_numb));
        }
    }

    return (
        <div className={'sample-organism-div'}>
            <form onSubmit={useQuery}>
                <div className={'sample-organism-input-container'}>
                    <label>Set samples count:</label>
                    <input
                        id="sampleNumberInput"
                        type="number"
                        step="1"
                        className={''}
                        placeholder={'0'}
                        required={true}
                        onChange={handleSampleNumber}
                    />
                </div>
                <div className={'sample-organism-input-container'}>
                    <label>Set rows count:</label>
                    <input
                        id="rowsCount"
                        type="number"
                        step="1"
                        className={''}
                        placeholder={'0'}
                        required={false}
                        onChange={handleIdListSize}
                    />
                </div>
                <button type={'submit'} onClick={() => {
                }} className={'data-generator-button'}>Show Results
                </button>
            </form>
            <ResultsOrganism postgreTimes={postgreTimes} mongoTimes={mongoTimes}/>
        </div>
    )
}