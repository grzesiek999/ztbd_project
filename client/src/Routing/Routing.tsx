import {type ReactElement} from 'react'
import {RouterProvider, createBrowserRouter, Route, createRoutesFromElements} from 'react-router-dom'
import {ROUTER_PATH} from "./RouterPath.tsx"
import WebsiteLayout from "../components/WebsiteLayout/WebsiteLayout.tsx";
import HomePage from "../components/Home/HomePage.tsx";
import SelectPage from "../components/Select/SelectPage.tsx";



const ROUTER = createBrowserRouter(
    createRoutesFromElements(
        <Route path='/' element={<WebsiteLayout />} >
            <Route path={ROUTER_PATH.HOME} element={<HomePage />} />
            <Route path={ROUTER_PATH.SELECT} element={<SelectPage />} />
            <Route path={ROUTER_PATH.CREATE} element={<HomePage />} />
            <Route path={ROUTER_PATH.UPDATE} element={<HomePage />} />
            <Route path={ROUTER_PATH.DELETE} element={<HomePage />} />
        </Route>
    )
)

export default function Router(): ReactElement {
    return <RouterProvider router={ROUTER} />
}