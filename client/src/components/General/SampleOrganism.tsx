import {SyntheticEvent, useState} from "react";
import ResultsOrganism from "./ResultsOrganism.tsx";


type SampleOrganismProps = {
    path: string
}

export default function SampleOrganism({path}: SampleOrganismProps) {

    const [sampleNumber, setSampleNumber] = useState<number>(0);
    const [idListSize, setIdListSize] = useState<number>(0);
    const [postgreTimes, setPostgreTimes] = useState<number[]>([]);
    const [mongoTimes, setMongoTimes] = useState<number[]>([]);

    const useSelect = async (e: SyntheticEvent) => {
        e.preventDefault();

        const response = await fetch(path, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                sampleNumber,
                idListSize
            })
        });
        if (response.ok) {
            const data = await response.json();

        } else { console.log(response.status, response.statusText); }
    }


    const handleIdListSize = (e: React.ChangeEvent<HTMLInputElement>) => {
        if(e.target.value === '') { setIdListSize(0); }
        else {
            const str_numb = e.target.value;
            setIdListSize(parseInt(str_numb));
        }
    }

    const handleSampleNumber = (e: React.ChangeEvent<HTMLInputElement>) => {
        if(e.target.value === '') { setSampleNumber(0); }
        else {
            const str_numb = e.target.value;
            setSampleNumber(parseInt(str_numb));
        }
    }

    return (
        <div className={'sample-organism-div'}>
            <form onSubmit={useSelect}>
                <div className={'sample-organism-input-container'}>
                    <label>Set id list size:</label>
                    <input
                        id="idListSizeInput"
                        type="number"
                        step="1"
                        className={''}
                        placeholder={'0'}
                        required={true}
                        onChange={handleIdListSize}
                    />
                </div>
                <div className={'sample-organism-input-container'}>
                    <label>Set sample number:</label>
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
                <button type={'submit'} onClick={() => {}} className={'data-generator-button'}>Show Results</button>
            </form>
            <ResultsOrganism postgreTimes={postgreTimes} mongoTimes={mongoTimes} />
        </div>
    )
}