import DataGenerator from "../DataGenerator/DataGenerator.tsx";
import UpdatePageContent from "./UpdatePageContent.tsx";


export default function UpdatePage() {
    return (
        <div className="select-page-div">
            <DataGenerator />
            <UpdatePageContent />
        </div>
    )
}