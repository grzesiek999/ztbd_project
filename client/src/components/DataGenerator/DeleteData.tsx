import {SyntheticEvent} from "react";


export default function DeleteData() {


    const clearDataBase = async (e: SyntheticEvent) => {
        e.preventDefault();

        const response = await fetch('http://127.0.0.1:8000/db/delete', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
        });
        if (response.ok) {

        } else {console.log(response.status, response.statusText)}
    }

    return (
        <div className={'delete-data-div'}>
            <form onSubmit={clearDataBase}>
                <button type={'submit'} onClick={() => {}} className={'data-generator-button'}>Usun dane z bazy danych</button>
            </form>
        </div>
    )
}