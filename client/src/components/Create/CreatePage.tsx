import DataGenerator from "../DataGenerator/DataGenerator.tsx";
import DeleteData from "../DataGenerator/DeleteData.tsx";
import CreatePageContent from "./CreatePageContent.tsx";


export default function CreatePage() {
    return (
        <div className="select-page-div">
            <DataGenerator />
            <DeleteData />
            <CreatePageContent />
        </div>
    )
}