import {SyntheticEvent, useEffect, useState} from "react";


export default function SelectPageContent() {

    const [usersByUserId, setUsersByUserId] = useState<boolean>(false);
    const [deviceByUserId, setDeviceByUserId] = useState<boolean>(false);
    const [deviceGestureByDeviceId, setDeviceGestureByUserId] = useState<boolean>(false);
    const [path, setPath] = useState<string>('');
    const id_list: number[] = [];

    const activeClass = 'active-button'
    const noActiveClass = 'no-active-button'
    const usersByUserIdPath = 'http://127.0.0.1:8000/totest/get_users_by_id_list';
    const deviceByUserIdPath = 'http://127.0.0.1:8000/totest/get_devices_by_user_id_list';
    const deviceGestureByDeviceIdPath = 'http://127.0.0.1:8000/totest/get_devices_by_user_id_list';

    useEffect(() => {
        if (usersByUserId) { setPath(usersByUserIdPath); }
        else if (deviceByUserId) { setPath(deviceByUserIdPath); }
        else if (deviceGestureByDeviceId) { setPath(deviceGestureByDeviceIdPath); }
        else { setPath(''); }
    }, [usersByUserId, deviceByUserId, deviceGestureByDeviceId])

    const useSelect = async (e: SyntheticEvent) => {
        e.preventDefault();

        const response = await fetch(path, {
            method: 'GET',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                id_list
            })
        });
        if (response.ok) {

        } else { console.log(response.status, response.statusText); }
    }

    return (
        <div className={"select-page-div-content"}>
            <div className={'button-options-choose-div'}>
                <button
                    type={"button"}
                    onClick={() => {
                        setUsersByUserId(true)
                        setDeviceByUserId(false)
                        setDeviceGestureByUserId(false)
                    }}
                    className={usersByUserId ? activeClass : noActiveClass}
                >SELECT users by user_id</button>
                <button
                    type={"button"}
                    onClick={() => {
                        setUsersByUserId(false)
                        setDeviceByUserId(true)
                        setDeviceGestureByUserId(false)
                    }}
                    className={deviceByUserId ? activeClass : noActiveClass}
                >SELECT users devices data by user_id</button>
                <button
                    type={"button"}
                    onClick={() => {
                        setUsersByUserId(false)
                        setDeviceByUserId(false)
                        setDeviceGestureByUserId(true)
                    }}
                    className={deviceGestureByDeviceId ? activeClass : noActiveClass}
                >SELECT devices gestures by device_id</button>
            </div>
            <div style={usersByUserId ? { display: 'flex' } : {display: 'none'}}>

            </div>
            <div style={deviceByUserId ? { display: 'flex' } : {display: 'none'}}>

            </div>
            <div style={deviceGestureByDeviceId ? { display: 'flex' } : {display: 'none'}}>

            </div>
        </div>
    )
}