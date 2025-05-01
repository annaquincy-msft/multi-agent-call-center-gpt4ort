import "./status-message.css";

type Properties = {
    isRecording: boolean;
};

export default function StatusMessage({ isRecording }: Properties) {
    if (!isRecording) {
        return <p
        className="text-black mb-4 mt-6 text-4x1 font bold"
        style={{
          textShadow: '1px 1px 0 white, -1px 1px 0 white, 1px -1px 0 white, -1px -1px 0 white',
        }}
      >
        Ask about your screening test.
      </p>;
    }

    return (
        <div className="flex items-center">
            <div className="relative h-6 w-6 overflow-hidden">
                <div className="absolute inset-0 flex items-end justify-around">
                    {[...Array(4)].map((_, i) => (
                        <div
                            key={i}
                            className="w-1 rounded-full bg-blue-600 opacity-80"
                            style={{
                                animation: `barHeight${(i % 3) + 1} 1s ease-in-out infinite`,
                                animationDelay: `${i * 0.1}s`
                            }}
                        />
                    ))}
                </div>
            </div>
            <p className="ext-black mb-4 mt-6 text-4x1 font bold"
            style={{
                textShadow: '1px 1px 0 white, -1px 1px 0 white, 1px -1px 0 white, -1px -1px 0 white',
              }}
              >Conversation in progress</p>
        </div>
    );
}
