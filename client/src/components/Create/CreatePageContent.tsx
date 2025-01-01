import {useEffect, useState} from "react";
import SampleOrganism from "../General/SampleOrganism.tsx";


export default function CreatePageContent() {

    const [addUsers, setAddUsers] = useState<boolean>(false);
    const [addDevices, setAddDevices] = useState<boolean>(false);
    const [addDevicesGestures, setAddDevicesGestures] = useState<boolean>(false);
    const [path, setPath] = useState<string>('');


    const activeClass = 'active-button'
    const noActiveClass = 'no-active-button'
    const addUsersPath = 'http://localhost:8000/test/insert/user';
    const addDevicesPath = 'http://localhost:8000/test/insert/device';
    const addDevicesGesturesPath = 'http://localhost:8000/test/insert/gesture';

    useEffect(() => {
        if (addUsers) { setPath(addUsersPath); }
        else if (addDevices) { setPath(addDevicesPath); }
        else if (addDevicesGestures) { setPath(addDevicesGesturesPath); }
        else { setPath(''); }
    }, [addUsers, addDevices, addDevicesGestures])


    return (
        <div className={"create-page-div-content"}>
            <div className={'button-options-choose-div'}>
                <button
                    type={"button"}
                    onClick={() => {
                        setAddUsers(true)
                        setAddDevices(false)
                        setAddDevicesGestures(false)
                    }}
                    className={addUsers ? activeClass : noActiveClass}
                >CREATE users</button>
                <button
                    type={"button"}
                    onClick={() => {
                        setAddUsers(false)
                        setAddDevices(true)
                        setAddDevicesGestures(false)
                    }}
                    className={addDevices ? activeClass : noActiveClass}
                >CREATE devices</button>
                <button
                    type={"button"}
                    onClick={() => {
                        setAddUsers(false)
                        setAddDevices(false)
                        setAddDevicesGestures(true)
                    }}
                    className={addDevicesGestures ? activeClass : noActiveClass}
                >CREATE devices gestures</button>
            </div>
            <SampleOrganism path={path} />
        </div>
    )
}