import {SyntheticEvent, useState} from "react";
import ResultsOrganism from "./ResultsOrganism.tsx";


type SampleOrganismProps = {
    path: string
}

export default function SampleOrganism({path}: SampleOrganismProps) {

    const [samples_count, set_samples_count] = useState<number>(0);
    const [rows_count, set_rows_count] = useState<number>(0);
    const [postgreTimes, setPostgreTimes] = useState<number[]>([]);
    const [mongoTimes, setMongoTimes] = useState<number[]>([]);
    const [sendData, setSendData] = useState<{}>({});

    const useQuery = async () => {
        setSendData({
            samples_count: samples_count !== 0 ? samples_count : null,
            rows_count: rows_count !== 0 ? rows_count : null,
        })

        const response = await fetch(path, {
            method: `POST`,
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(sendData)
        });
        if (response.ok) {
            const data = await response.json();

        } else { console.log(response.status, response.statusText); }
    }


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
                        required={true}
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