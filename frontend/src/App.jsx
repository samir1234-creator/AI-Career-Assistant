import { AnalyzerPage } from './pages/AnalyzerPage';
import { MainLayout } from './layouts/MainLayout';

function App() {
  return (
    <div className="App">
      <MainLayout>
        <AnalyzerPage />
      </MainLayout>
    </div>
  )
}

export default App;
