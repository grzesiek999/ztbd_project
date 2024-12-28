import {Link} from "react-router-dom";
import {ROUTER_PATH} from "../../Routing/RouterPath.tsx";


export  default function LayoutNav() {
    return (
        <div className={'website-layout-nav'}>
            <h1><Link to={ROUTER_PATH.HOME}>PostgreSQL vs MongoDB</Link></h1>
            <div className={'website-layout-nav-list-div'}>
                <ul>
                    <li><Link to={ROUTER_PATH.SELECT}>SELECT</Link></li>
                    <li><Link to={ROUTER_PATH.CREATE}>CREATE</Link></li>
                    <li><Link to={ROUTER_PATH.UPDATE}>UPDATE</Link></li>
                    <li><Link to={ROUTER_PATH.DELETE}>DELETE</Link></li>
                </ul>
            </div>
        </div>
    )
}