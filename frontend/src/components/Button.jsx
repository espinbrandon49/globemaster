export default function Button({
  children,
  onClick,
  type = "button",
  disabled = false,
  className = "",
}) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded flex items-center justify-center
        disabled:opacity-50 disabled:cursor-not-allowed
        transition-all duration-200 ease-in-out
        focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2
        hover:shadow-md active:scale-[0.98] ${className}`}
    >
      {children}
    </button>
  );
}