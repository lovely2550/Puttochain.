export default function Dashboard() {
  return (
    <div className="p-6 grid grid-cols-1 gap-6">
      <h1 className="text-3xl font-bold">Nibbāna Dashboard</h1>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="p-4 rounded-2xl shadow bg-white">Karma Score</div>
        <div className="p-4 rounded-2xl shadow bg-white">Meditation Logs</div>
        <div className="p-4 rounded-2xl shadow bg-white">Nibbāna Progress</div>
      </div>
    </div>
  );
}