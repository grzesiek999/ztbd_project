import DataGenerator from "../DataGenerator/DataGenerator.tsx";
import DeleteData from "../DataGenerator/DeleteData.tsx";
import DeletePageContent from "./DeletePageContent.tsx";


export default function DeletePage() {
    return (
        <div className="select-page-div">
            <DataGenerator />
            <DeleteData />
            <DeletePageContent />
        </div>
    )
}