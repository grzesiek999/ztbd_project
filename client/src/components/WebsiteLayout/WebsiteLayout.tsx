import {Outlet} from "react-router-dom";
import LayoutNav from "./LayoutNav.tsx";


export default function WebsiteLayout() {
    return (
        <div className={'website-div'}>
            <header>
                <LayoutNav />
            </header>
            <Outlet/>
        </div>
    )
}