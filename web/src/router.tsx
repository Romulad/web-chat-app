import { createBrowserRouter } from "react-router-dom";

import { 
  ErrorPage,
  CreateAccountPage,
  HomePage,
  OpenChatChatPage
} from "./pages";
import { 
  chatInterfacePath,
  createAccountPath, 
  homePath,
  openChatHomePath,
  openChatPath
} from "./lib/paths";
import OpenChatPage from "./pages/openChatPage";
import ProtectedRoute from "./protectRoutes";
import ChatInterface from "./pages/chatInterface";


const router = createBrowserRouter([
  {
    path: homePath,
    element: <HomePage />,
    errorElement: <ErrorPage />,
  },
  {
    path: createAccountPath,
    element: <CreateAccountPage />,
    errorElement: <ErrorPage />,
  },
  {
    path: openChatPath,
    element: <OpenChatChatPage />,
    errorElement: <ErrorPage />,
  },
  {
    path: openChatHomePath,
    element: <OpenChatPage />,
    errorElement: <ErrorPage />,
  },
  {
    path: chatInterfacePath,
    element: <ProtectedRoute children={<ChatInterface />} />,
    errorElement: <ErrorPage />,
  },
]);

export default router;