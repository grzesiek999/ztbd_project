

type TableOfDataProps = {
    title: string;
    timesArray: number[];
}

const TableOfData = ({title, timesArray}: TableOfDataProps) => {
    const labels = Array.from(
        { length: timesArray.length },
        (_, index) => `Sample ${index + 1}`
    );

    return (
        <div className="tableOfData-div">
            <span className={'table-title-span'}>{title}</span>
            <ul>
                {labels.map((label, index) => (
                    <li key={index}>
                        <p className={'temp'}>{label}</p>
                        <p>{timesArray[index]} ms</p>
                    </li>
                ))}
            </ul>

        </div>
    )
}


export default TableOfData;