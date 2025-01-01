import DataGenerator from "../DataGenerator/DataGenerator.tsx";
import SelectPageContent from "./SelectPageContent.tsx";


export default function SelectPage() {
    return (
        <div className="select-page-div">
            <DataGenerator />
            <SelectPageContent />
        </div>
    )
}