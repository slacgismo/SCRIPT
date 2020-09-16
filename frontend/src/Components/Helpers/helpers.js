// Helper functions

export function processResults(resultArr) {
    const data_to_visualize_all = [];
    let isTimeSeries = false;

    if (resultArr[0][0] != undefined && resultArr[0][0].length === 0) {
        isTimeSeries = false;
    } else if (resultArr.length == 0) {
        isTimeSeries = false;
    } else if (resultArr[0][Object.keys(resultArr[0])[0]][0].time) {
        isTimeSeries = true;
    } else {
        isTimeSeries = false;
    }

    for (const result of resultArr) {
        const data_to_visualize = {};

        for (const field of Object.keys(result)) {
            const data = result[field];
            const dataFormatted = data.map((datapoint, i) => (
                {
                    x: isTimeSeries ? i : datapoint.year,
                    y: isTimeSeries ? parseFloat(datapoint.load) : parseFloat(datapoint.data)
                }   
            ));
            data_to_visualize[field] = {
                yAxis: `${field}`.replace(/_/g, " "),
                unit: "Power (kW)",
                xAxis: isTimeSeries ? "Time" : "Year",
                data: dataFormatted,
            };
        }
        data_to_visualize_all.push(data_to_visualize);
    }
    return data_to_visualize_all;
}

export function preprocessData(allData) {
    const data = allData.dataValues;
    const fields = data[0] ? Object.keys(data[0].values): [0];

    // Init result
    const result = {};
    for (const field of fields) {
        result[field] = [];
    }
    data.forEach(dataItem => {
        const year = dataItem.config.year;
        const allFields = dataItem.values;
        for (const field of fields) {
            result[field].push({
                year: year,
                data: parseFloat(allFields[field]),
            });
        }
    });
    const resultFlattened = [];
    for (const field of fields) {
        resultFlattened.push({
            [field]: result[field],
        });
    }
    return resultFlattened;
}
