module hdf5_io

    use hdf5

!---------------------------------------------------------------------------------------------

contains

    !! Open
    subroutine h5_open(path, file_id)

        ! Open an HDF5 file.
        !
        ! Input:
        ! - path (character): File Path
        !
        ! Output:
        ! -  file_id (HID_T): File Identifier
        !
        ! Used by:
        ! - solvers.llg.run_Microstates
        ! - solvers.llg.run_MvsH
        ! - solvers.llg.run_MvsT
        ! - solvers.llg-t.run_Microstates
        ! - solvers.llg-t.run_MvsH
        ! - solvers.llg-t.run_MvsT
        !
        ! Last Updated: 
        ! - 16/08/2026

        character(len=*), intent(in) :: path
        integer(HID_T), intent(out)  :: file_id
        integer(HID_T)               :: fapl_id
        integer                      :: error

        call h5open_f(error)
        call h5pcreate_f(H5P_FILE_ACCESS_F, fapl_id, error)
        call h5pset_libver_bounds_f(fapl_id, H5F_LIBVER_LATEST_F, H5F_LIBVER_LATEST_F, error)
        call h5fopen_f(path, H5F_ACC_RDWR_F, file_id, error, access_prp=fapl_id)
        call h5pclose_f(fapl_id, error)

    end subroutine

!---------------------------------------------------------------------------------------------

    !! Close
    subroutine h5_close(file_id)

        ! Close an HDF5 file.
        !
        ! Input:
        ! - file_id (HID_T): File Identifier
        !
        ! Output:
        ! - None
        !
        ! Used by:
        ! - solvers.llg.run_Microstates
        ! - solvers.llg.run_MvsH
        ! - solvers.llg.run_MvsT
        ! - solvers.llg-t.run_Microstates
        ! - solvers.llg-t.run_MvsH
        ! - solvers.llg-t.run_MvsT
        !
        ! Last Updated: 
        ! - 16/08/2026

        integer(HID_T), intent(in) :: file_id
        integer                    :: error

        call h5fclose_f(file_id, error)
        call h5close_f(error)

    end subroutine

!---------------------------------------------------------------------------------------------

    !! Read 1D Dataset
    subroutine h5_read_1d(path, file_id, n, dataset)

        ! Read a 1D dataset.
        !
        ! Input:
        ! -                 path (character): File Path
        ! -                  file_id (HID_T): File Identifier
        ! -                      n (integer): Number of Rows(F)/Columns(Py)
        !
        ! Output:
        ! - dataset ((real*8, ), array[n, ]): Dataset
        !
        ! Used by:
        ! - solvers.llg.run_Microstates
        ! - solvers.llg.run_MvsH
        ! - solvers.llg.run_MvsT
        ! - solvers.llg-t.run_Microstates
        ! - solvers.llg-t.run_MvsH
        ! - solvers.llg-t.run_MvsT
        !
        ! Last Updated: 
        ! - 16/08/2026

        character(len=*), intent(in) :: path
        integer(HID_T), intent(in)   :: file_id
        integer, intent(in)          :: n
        real*8, intent(out)          :: dataset(n)
        integer(HID_T)               :: dataset_id
        integer(HSIZE_T)             :: dimensions(1)
        integer                      :: error

        dimensions(1) = n
        call h5dopen_f(file_id, path, dataset_id, error)
        call h5dread_f(dataset_id, H5T_NATIVE_DOUBLE, dataset, dimensions, error)
        call h5dclose_f(dataset_id, error)

    end subroutine

!---------------------------------------------------------------------------------------------

    !! Read 2D Dataset
    subroutine h5_read_2d(path, file_id, n, m, dataset)

        ! Read a 2D dataset.
        !
        ! Input:
        ! -                        path (character): File Path
        ! -                         file_id (HID_T): File Identifier
        ! -                             n (integer): Number of Rows(F)/Columns(Py)
        ! -                             m (integer): Number of Columns(F)/Rows(Py)
        !
        ! Output:
        ! - dataset ((real*8, real*8), array[n, m]): Dataset
        !
        ! Used by:
        ! - solvers.llg.run_Microstates
        ! - solvers.llg.run_MvsH
        ! - solvers.llg.run_MvsT
        ! - solvers.llg-t.run_Microstates
        ! - solvers.llg-t.run_MvsH
        ! - solvers.llg-t.run_MvsT
        !
        ! Last Updated: 
        ! - 16/08/2026

        character(len=*), intent(in) :: path
        integer(HID_T), intent(in)   :: file_id
        integer, intent(in)          :: n, m
        real*8, intent(out)          :: dataset(n, m)
        integer(HID_T)               :: dataset_id
        integer(HSIZE_T)             :: dimensions(2)
        integer                      :: error

        dimensions = [n, m]
        call h5dopen_f(file_id, path, dataset_id, error)
        call h5dread_f(dataset_id, H5T_NATIVE_DOUBLE, dataset, dimensions, error)
        call h5dclose_f(dataset_id, error)

    end subroutine

!---------------------------------------------------------------------------------------------

    !! Write 1D Dataset
    subroutine h5_write_1d(path, file_id, n, dataset)

        ! Write a 1D dataset.
        !
        ! Input:
        ! -                 path (character): File Path
        ! -                  file_id (HID_T): File Identifier
        ! -                      n (integer): Number of Rows(F)/Columns(Py)
        ! - dataset ((real*8, ), array[n, ]): Dataset
        !
        ! Output:
        ! - None
        !
        ! Used by:
        ! - solvers.llg.run_Microstates
        ! - solvers.llg.run_MvsH
        ! - solvers.llg.run_MvsT
        ! - solvers.llg-t.run_Microstates
        ! - solvers.llg-t.run_MvsH
        ! - solvers.llg-t.run_MvsT
        !
        ! Last Updated: 
        ! - 16/08/2026

        character(len=*), intent(in) :: path
        integer(HID_T), intent(in)   :: file_id
        integer, intent(in)          :: n
        real*8, intent(in)           :: dataset(n)
        integer(HID_T)               :: dataset_id, space_id
        integer(HSIZE_T)             :: dimensions(1)
        integer                      :: error

        dimensions(1) = n
        call h5screate_simple_f(1, dimensions, space_id, error)
        call h5dcreate_f(file_id, path, H5T_NATIVE_DOUBLE, space_id, dataset_id, error)
        call h5dwrite_f(dataset_id, H5T_NATIVE_DOUBLE, dataset, dimensions, error)
        call h5dclose_f(dataset_id, error)
        call h5sclose_f(space_id, error)

    end subroutine

!---------------------------------------------------------------------------------------------

    !! Write 2D Dataset
    subroutine h5_write_2d(path, file_id, n, m, dataset)

        ! Write a 2D dataset.
        !
        ! Input:
        ! -                        path (character): File Path
        ! -                         file_id (HID_T): File Identifier
        ! -                             n (integer): Number of Rows(F)/Columns(Py)
        ! -                             m (integer): Number of Columns(F)/Rows(Py)
        ! - dataset ((real*8, real*8), array[n, m]): Dataset
        !
        ! Output:
        ! - None
        !
        ! Used by:
        ! - solvers.llg.run_Microstates
        ! - solvers.llg.run_MvsH
        ! - solvers.llg.run_MvsT
        ! - solvers.llg-t.run_Microstates
        ! - solvers.llg-t.run_MvsH
        ! - solvers.llg-t.run_MvsT
        !
        ! Last Updated: 
        ! - 16/08/2026

        character(len=*), intent(in) :: path
        integer(HID_T), intent(in)   :: file_id
        integer, intent(in)          :: n, m
        real*8, intent(in)           :: dataset(n, m)
        integer(HID_T)               :: dataset_id, space_id
        integer(HSIZE_T)             :: dimensions(2)
        integer                      :: error

        dimensions = [n, m]
        call h5screate_simple_f(2, dimensions, space_id, error)
        call h5dcreate_f(file_id, path, H5T_NATIVE_DOUBLE, space_id, dataset_id, error)
        call h5dwrite_f(dataset_id, H5T_NATIVE_DOUBLE, dataset, dimensions, error)
        call h5dclose_f(dataset_id, error)
        call h5sclose_f(space_id, error)

    end subroutine

!---------------------------------------------------------------------------------------------

end module hdf5_io