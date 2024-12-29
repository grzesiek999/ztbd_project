import {useEffect, useState} from "react";
import SampleOrganism from "../General/SampleOrganism.tsx";


export default function UpdatePageContent() {

    const [updateUsers, setUpdateUsers] = useState<boolean>(false);
    const [updateDevices, setUpdateDevices] = useState<boolean>(false);
    const [updateGesture, setUpdateGesture] = useState<boolean>(false);
    const [path, setPath] = useState<string>('');


    const activeClass = 'active-button'
    const noActiveClass = 'no-active-button'
    const updateUsersPath = '';
    const updateDevicesPath = '';
    const updateGesturePath = '';

    useEffect(() => {
        if (updateUsers) { setPath(updateUsersPath); }
        else if (updateDevices) { setPath(updateDevicesPath); }
        else if (updateGesture) { setPath(updateGesturePath); }
        else { setPath(''); }
    }, [updateUsers, updateDevices, updateGesture])


    return (
        <div className={"update-page-div-content"}>
            <div className={'button-options-choose-div'}>
                <button
                    type={"button"}
                    onClick={() => {
                        setUpdateUsers(true)
                        setUpdateDevices(false)
                        setUpdateGesture(false)
                    }}
                    className={updateUsers ? activeClass : noActiveClass}
                >UPDATE users</button>
                <button
                    type={"button"}
                    onClick={() => {
                        setUpdateUsers(false)
                        setUpdateDevices(true)
                        setUpdateGesture(false)
                    }}
                    className={updateDevices ? activeClass : noActiveClass}
                >UPDATE devices</button>
                <button
                    type={"button"}
                    onClick={() => {
                        setUpdateUsers(false)
                        setUpdateDevices(false)
                        setUpdateGesture(true)
                    }}
                    className={updateGesture ? activeClass : noActiveClass}
                >UPDATE gesture</button>
            </div>
            <SampleOrganism path={path} />
        </div>
    )
}