import TVChartContainer from 'components/common/TVChartContainer';
import * as Datafeed from 'containers/DataFeed';

import './App.css';

function App() {
  // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access, @typescript-eslint/no-explicit-any
  return (
    <div className="App">
      <div className="App-body">
        <TVChartContainer datafeed={Datafeed} />
      </div>
    </div>
  );
}

export default App;
