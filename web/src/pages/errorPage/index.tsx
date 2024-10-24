import { useRouteError } from "react-router-dom";

export default function ErrorPage() {
  const error : any = useRouteError();
  console.error(error);

  return (
    <div className="h-screen flex flex-col gap-3 items-center justify-center text-center">
      <div>
        <h1>Oops!</h1>
        <p>Sorry, an unexpected error has occurred.</p>
      </div>

      <p>
        <i>{error?.statusText || error?.message || ""}</i>
      </p>
    </div>
  );
}