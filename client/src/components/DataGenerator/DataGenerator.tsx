import {SyntheticEvent, useEffect, useState} from "react";


export default function DataGenerator() {

    const [user_count, setUserCount] = useState<number>(0)
    const [deviceCount, setDeviceCount] = useState<number>(0)
    const [gestureCount, setGestureCount] = useState<number>(0)
    const [log_count, setLogCount] = useState<number>(0)


    const [device_count_range, setDeviceCountRange] = useState([0, 0]);
    const [gesture_count_range, setGestureCountRange] = useState([0, 0]);


    const importData = async (e: SyntheticEvent) => {
        e.preventDefault();

        const response = await fetch('http://127.0.0.1:8000/db/import', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                user_count,
                device_count_range,
                gesture_count_range,
                log_count
            })
        });
        if (response.ok) {

        } else {console.log(response.status, response.statusText)}
    }

    const handleUserCount = (e: React.ChangeEvent<HTMLInputElement>) => {
        if(e.target.value === '') { setUserCount(0); }
        else {
            const str_numb = e.target.value;
            setUserCount(parseInt(str_numb));
        }
    }

    const handleDeviceCountRange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if(e.target.value === '') { setDeviceCount(0); }
        else {
            const str_numb = e.target.value;
            setDeviceCount(parseInt(str_numb));
        }
    }

    const handleGestureCountRange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if(e.target.value === '') { setGestureCount(0); }
        else {
            const str_numb = e.target.value;
            setGestureCount(parseInt(str_numb));
        }
    }

    const handleLogCount = (e: React.ChangeEvent<HTMLInputElement>) => {
        if(e.target.value === '') { setLogCount(0); }
        else {
            const str_numb = e.target.value;
            setLogCount(parseInt(str_numb));
        }
    }

    useEffect(() => {
        setDeviceCountRange([0, deviceCount]);
        setGestureCountRange([0, gestureCount]);
    }, [deviceCount, gestureCount]);


    return (
        <div className={'data-generator-div'}>
            <form onSubmit={importData}>
                <span>Wprowadz dane</span>
                <label>User count:</label>
                <input
                    id="userCountInput"
                    type="number"
                    step="1"
                    className={''}
                    placeholder={'0'}
                    required={true}
                    onChange={handleUserCount}
                />
                <label>Device count:</label>
                <input
                    id="deviceCountInput"
                    type="number"
                    step="1"
                    className={''}
                    placeholder={'0'}
                    required={true}
                    onChange={handleDeviceCountRange}
                />
                <label>Gesture count:</label>
                <input
                    id="gestureCountInput"
                    type="number"
                    step="1"
                    className={''}
                    placeholder={'0'}
                    required={true}
                    onChange={handleGestureCountRange}
                />
                <label>Log count:</label>
                <input
                    id="logCountInput"
                    type="number"
                    step="1"
                    className={''}
                    placeholder={'0'}
                    required={true}
                    onChange={handleLogCount}
                />
                <button type={'submit'} onClick={()=>{} } className={'data-generator-button'}>Wygeneruj i zaimportuj dane</button>
            </form>
        </div>
    )
}