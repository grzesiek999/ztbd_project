import {SyntheticEvent, useEffect, useState} from "react";


export default function DeletePageContent() {

    const [deleteUsersByUserId, setDeleteUsersByUserId] = useState<boolean>(false);
    const [deleteDeviceByDeviceId, setDeleteDeviceByDeviceId] = useState<boolean>(false);
    const [deleteDeviceGestureByGestureType, setDeleteDeviceGestureByGestureType] = useState<boolean>(false);
    const [path, setPath] = useState<string>('');
    const id_list: number[] = [];
    const [gestureType, setGestureType] = useState<string>('');
    const [dataToSend, setDataToSend] = useState<string | number[]>();

    const activeClass = 'active-button'
    const noActiveClass = 'no-active-button'
    const deleteUsersByUserIdPath = '';
    const deleteDeviceByDeviceIdPath = '';
    const deleteDeviceGestureByGestureTypePath = '';

    useEffect(() => {
        if (deleteUsersByUserId) { setPath(deleteUsersByUserIdPath); setDataToSend(id_list); }
        else if (deleteDeviceByDeviceId) { setPath(deleteDeviceByDeviceIdPath); setDataToSend(id_list); }
        else if (deleteDeviceGestureByGestureType) { setPath(deleteDeviceGestureByGestureTypePath); setDataToSend(gestureType); }
        else { setPath(''); }
    }, [deleteUsersByUserId, deleteDeviceByDeviceId, deleteDeviceGestureByGestureType])

    const useDelete = async (e: SyntheticEvent) => {
        e.preventDefault();

        const response = await fetch(path, {
            method: 'DELETE',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                dataToSend
            })
        });
        if (response.ok) {

        } else { console.log(response.status, response.statusText); }
    }

    return (
        <div className={"delete-page-div-content"}>
            <div className={'button-options-choose-div'}>
                <button
                    type={"button"}
                    onClick={() => {
                        setDeleteUsersByUserId(true)
                        setDeleteDeviceByDeviceId(false)
                        setDeleteDeviceGestureByGestureType(false)
                    }}
                    className={deleteUsersByUserId ? activeClass : noActiveClass}
                >DELETE users by user id</button>
                <button
                    type={"button"}
                    onClick={() => {
                        setDeleteUsersByUserId(false)
                        setDeleteDeviceByDeviceId(true)
                        setDeleteDeviceGestureByGestureType(false)
                    }}
                    className={deleteDeviceByDeviceId ? activeClass : noActiveClass}
                >DELETE devices by device id</button>
                <button
                    type={"button"}
                    onClick={() => {
                        setDeleteUsersByUserId(false)
                        setDeleteDeviceByDeviceId(false)
                        setDeleteDeviceGestureByGestureType(true)
                    }}
                    className={deleteDeviceGestureByGestureType ? activeClass : noActiveClass}
                >DELETE devices gestures by gesture type</button>
            </div>
            <div style={deleteUsersByUserId ? { display: 'flex' } : {display: 'none'}}>

            </div>
            <div style={deleteDeviceByDeviceId ? { display: 'flex' } : {display: 'none'}}>

            </div>
            <div style={deleteDeviceGestureByGestureType ? { display: 'flex' } : {display: 'none'}}>

            </div>
        </div>
    )
}