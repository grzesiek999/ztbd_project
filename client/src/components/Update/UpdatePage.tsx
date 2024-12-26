import DataGenerator from "../DataGenerator/DataGenerator.tsx";
import DeleteData from "../DataGenerator/DeleteData.tsx";
import UpdatePageContent from "./UpdatePageContent.tsx";


export default function UpdatePage() {
    return (
        <div className="select-page-div">
            <DataGenerator />
            <DeleteData />
            <UpdatePageContent />
        </div>
    )
}