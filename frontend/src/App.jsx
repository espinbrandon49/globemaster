import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import StartPage from './pages/StartPage'
import PlayerForm from './pages/PlayerForm'
import GameInit from './pages/GameInit'
import GamePlay from './pages/GamePlay'
import Summary from './pages/Summary'
import TopSessionScores from "./pages/TopSessionScores"
import NotFound from './pages/NotFound'


function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<StartPage />} />
        <Route path='/create-player' element={<PlayerForm />} />
        <Route path='/init' element={<GameInit />} />
        <Route path='/play' element={<GamePlay />} />
        <Route path='/summary' element={<Summary />} />
        <Route path='/leaderboard' element={<TopSessionScores />} />
        <Route path='*' element={<NotFound />} />
      </Routes>
    </Router>
  )
}

export default App
