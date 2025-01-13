import {Outlet} from "react-router-dom";
import LayoutNav from "./LayoutNav.tsx";


export default function WebsiteLayout() {
    return (
        <div className={'website-div'}>
            <header>
                <LayoutNav />
            </header>
            <main>
                <Outlet/>
            </main>
            <footer>
            <span className="authors-span">Autorzy: Sylwia Zemła, Grzegorz Pasich</span>
            </footer>
        </div>
    )
}