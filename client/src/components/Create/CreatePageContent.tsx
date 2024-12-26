import {SyntheticEvent, useEffect, useState} from "react";


export default function CreatePageContent() {

    const [addUsers, setAddUsers] = useState<boolean>(false);
    const [addDevices, setAddDevices] = useState<boolean>(false);
    const [addDevicesGestures, setAddDevicesGestures] = useState<boolean>(false);
    const [path, setPath] = useState<string>('');
    const [numberOfAttempts, setNumberOfAttempts] = useState<number | null>(null);

    const activeClass = 'active-button'
    const noActiveClass = 'no-active-button'
    const addUsersPath = '';
    const addDevicesPath = '';
    const addDevicesGesturesPath = '';

    useEffect(() => {
        if (addUsers) { setPath(addUsersPath); }
        else if (addDevices) { setPath(addDevicesPath); }
        else if (addDevicesGestures) { setPath(addDevicesGesturesPath); }
        else { setPath(''); }
    }, [addUsers, addDevices, addDevicesGestures])

    const useCreate = async (e: SyntheticEvent) => {
        e.preventDefault();

        const response = await fetch(path, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                numberOfAttempts
            })
        });
        if (response.ok) {

        } else { console.log(response.status, response.statusText); }
    }

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
            <div style={addUsers ? { display: 'flex' } : {display: 'none'}}>

            </div>
            <div style={addDevices ? { display: 'flex' } : {display: 'none'}}>

            </div>
            <div style={addDevicesGestures ? { display: 'flex' } : {display: 'none'}}>

            </div>
        </div>
    )
}