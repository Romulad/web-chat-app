import React, { createContext, useContext, useState } from "react"


type mobileUiStateContextType = {
    showChatInterface: boolean,
    toggleChartInterface: () => void
}

const contextDefaultValue : mobileUiStateContextType = {
    showChatInterface: true,
    toggleChartInterface: () => {}
}

const mobileUiStateContext = createContext<mobileUiStateContextType>(contextDefaultValue);

export function useMobileUiContext(){
    const contextData = useContext(mobileUiStateContext);
    return contextData
}

export function MobileUiStateContextProvider({ children } : { children: React.ReactNode }){
    const [showChatInterface, setShowChatInterface] = useState(true);

    function toggleChartInterface(){
        setShowChatInterface(!showChatInterface)
    }

    const providerValue = {
        showChatInterface,
        toggleChartInterface
    }

    return(
        <mobileUiStateContext.Provider value={providerValue}>
            {children}
        </mobileUiStateContext.Provider>
    )
}