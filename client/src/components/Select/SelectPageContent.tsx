import {useEffect, useState} from "react";
import SampleOrganism from "../General/SampleOrganism.tsx";


export default function SelectPageContent() {

    const [usersByUserId, setUsersByUserId] = useState<boolean>(false);
    const [deviceByUserId, setDeviceByUserId] = useState<boolean>(false);
    const [deviceGestureByDeviceId, setDeviceGestureByUserId] = useState<boolean>(false);
    const [path, setPath] = useState<string>('');


    const activeClass = 'active-button'
    const noActiveClass = 'no-active-button'
    const usersByUserIdPath = 'http://localhost:8000/test/select/user';
    const deviceByUserIdPath = 'http://localhost:8000/test/select/device';
    const deviceGestureByDeviceIdPath = 'http://localhost:8000/test/select/device_gestures';

    useEffect(() => {
        if (usersByUserId) { setPath(usersByUserIdPath); }
        else if (deviceByUserId) { setPath(deviceByUserIdPath); }
        else if (deviceGestureByDeviceId) { setPath(deviceGestureByDeviceIdPath); }
        else { setPath(''); }
    }, [usersByUserId, deviceByUserId, deviceGestureByDeviceId])


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
                >SELECT users</button>
                <button
                    type={"button"}
                    onClick={() => {
                        setUsersByUserId(false)
                        setDeviceByUserId(true)
                        setDeviceGestureByUserId(false)
                    }}
                    className={deviceByUserId ? activeClass : noActiveClass}
                >SELECT devices</button>
                <button
                    type={"button"}
                    onClick={() => {
                        setUsersByUserId(false)
                        setDeviceByUserId(false)
                        setDeviceGestureByUserId(true)
                    }}
                    className={deviceGestureByDeviceId ? activeClass : noActiveClass}
                >SELECT device gestures</button>
            </div>
            <SampleOrganism path={path}  httpMethod={"POST"}/>
        </div>
    )
}