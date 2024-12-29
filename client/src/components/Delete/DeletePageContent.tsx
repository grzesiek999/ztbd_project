import {useEffect, useState} from "react";
import SampleOrganism from "../General/SampleOrganism.tsx";


export default function DeletePageContent() {

    const [deleteUsersByUserId, setDeleteUsersByUserId] = useState<boolean>(false);
    const [deleteDeviceByDeviceId, setDeleteDeviceByDeviceId] = useState<boolean>(false);
    const [deleteDeviceGestureByGestureType, setDeleteDeviceGestureByGestureType] = useState<boolean>(false);
    const [path, setPath] = useState<string>('');


    const activeClass = 'active-button'
    const noActiveClass = 'no-active-button'
    const deleteUsersByUserIdPath = '';
    const deleteDeviceByDeviceIdPath = '';
    const deleteDeviceGestureByGestureTypePath = '';

    useEffect(() => {
        if (deleteUsersByUserId) { setPath(deleteUsersByUserIdPath); }
        else if (deleteDeviceByDeviceId) { setPath(deleteDeviceByDeviceIdPath); }
        else if (deleteDeviceGestureByGestureType) { setPath(deleteDeviceGestureByGestureTypePath); }
        else { setPath(''); }
    }, [deleteUsersByUserId, deleteDeviceByDeviceId, deleteDeviceGestureByGestureType])


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
            <SampleOrganism path={path} />
        </div>
    )
}