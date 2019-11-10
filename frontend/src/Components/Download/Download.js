import React from 'react';
import Base from "../../Layouts/Base";


class Download extends React.Component {
	constructor(props) {
		super(props);
	}
	
	downloadScript = () => {
		fetch('http://localhost:8080/employees/download') /* TODO download from which url */
			.then(response => {
				response.blob().then(blob => {
					let url = window.URL.createObjectURL(blob);
					let a = document.createElement('a');
					a.href = url;
					a.download = 'employees.json'; /* TODO download file name */
					a.click();
				});
				window.location.href = response.url;
		});
	}
	
	render() {
		return (
			<div>
				<Base 
					content = {
						<div>
							<p>Download Script</p>
							<button onClick={this.downloadScript}>Download</button>
							<p/>    
						</div>
					}
				/>
			</div>
		);
	}
}

export default Download;