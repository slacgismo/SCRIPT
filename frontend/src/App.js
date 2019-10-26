import React, {Component} from 'react';
import Paperbase from './Layouts/Base'

class App extends Component {
    page = "overview";
    render() {
        return (
            <div >
                <Paperbase />
            </div>
        );
    }
}

export default App;